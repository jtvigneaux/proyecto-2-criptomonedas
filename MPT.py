from keccak_hash import keccak_hash
from path import Path
from nodes import Node, Leaf, Branch, Extension


class MPT:

    def __init__(self, nodes, root=None):
        self.nodes = nodes
        self.root = root

    # Metodos que se pueden llamar desde afuera
    def get_node_data(self, key):
        if not self.root:
            return

        hash_key = keccak_hash(key)
        #print(hash_key) 
        path = Path(hash_key)

        node = self.get(self.root, path)
        
        return node.value

    def update_trie(self, key, value):
        hash_key = keccak_hash(key)
        print("Hash editado:", hash_key.hex())

        node_path = Path(hash_key)
        result = self.update(self.root, node_path, value)

        self.root = result

    # Métodos que sólo se llaman dentro de la clase
    def get_node(self, ref):
    	encode_node = self.nodes[ref]
    	return Node.decode(encode_node)

    def get(self, node_ref, path):
        node = self.get_node(node_ref)

        if not len(path):
            return node
        
        if isinstance(node, Leaf):
            if node.path == path:
                return node
        
        elif isinstance(node, Extension):
            # Hay que llamar recursivamente
            if path.is_prefix(node.path):
                new_path = path.add_offset(len(node.path))
                return self.get(node.next_node, new_path)
        
        elif isinstance(node, Branch):
            branch = node.branches[path[0]]
            if len(branch) > 0:
                return self.get(branch, path.add_offset(1))

    def update(self, node_ref, path, value):
        # Si no hay un nodo de referencia
        if not node_ref:
            # Guardar un nuevo nodo hoja y retornarlo
            return self.save_node(Leaf(path, value))
        
        node = self.get_node(node_ref)
        
        if isinstance(node, Leaf):
       	    # Está la opción de que se este actualizando un nodo hoja o que se este creando
       	    if node.path == path:
       		    node.value = value
       		    return self.save_node(node)

            # Encontrar ruta comun
            common_path = path.common_path(node.path)

            # Acortar lo que ambos path tienen en comun
            path.add_offset(len(common_path))
            node.path.add_offset(len(common_path))

            # Hay que crear un branch node que almacene los dos leaf
            reference = self.create_branch(path, value, node.path, node.value)

            # Revisar si hay ruta en comun. En el caso de haber crear un nodo de extensión
            if len(common_path):
                return self.save_node(Extension(common_path, reference))
            return reference

        elif isinstance(node, Extension):
            # Puede pasar que el nuevo nodo tenga el mismo principio que el nodo de extension, 
            # en ese caso solo se va a agregar. La otra opción es que no coincidan y en ese caso hay 
            # que separar el nodo
            if path.is_prefix(node.path):
                updated_reference = self.update(node.next_node, path.add_offset(len(node.path)), value)
                return self.save_node(Extension(node.path, updated_reference))

            # Separar el nodo
            common_path = path.common_path(node.path)

            # Acortar lo que ambos path tienen en comun
            path.add_offset(len(common_path))
            node.path.add_offset(len(common_path))

            # Hay que crear una nueva branch
            branches = [b""] * 16

            if not len(path):
                branch_value = value     
            else:
                branch_value = b""
                self.create_leaf(path, value, branches)

            # Crear el nodo de extension que se desplazo
            self.create_extension(node.path, node.next_node, branches)

            reference = self.save_node(Branch(branches, branch_value))

            if len(common_path):
                return self.save_node(Extension(common_path, reference))
            return reference
        
        elif isinstance(node, Branch):
            # Las dos opciones que hay aca son que el path este vacío y en ese caso sólo hay que actualizar 
            # el valor del nodo o que no este vacío y ahi hay que llamar a la función recursiva
            if len(path) == 0:
                return self.save_node(Branch(node.branches, value))
            
            _id = path[0]
            updated_reference = self.update(node.branches[_id], path.add_offset(1), value)

            node.branches[_id] = updated_reference

            return self.save_node(node)

    def create_branch(self, path1, value1, path2, value2):
        # Lista con los valores de todos los branches
        branches = [b""] * 16

        # Si alguno de los dos path es nulo, entonces el valor que se de 
        # se debe almacenar en este nodo
        branch_value = b""
        if not len(path1):
            branch_value = value1
        elif not len(path2):
            branch_value = value2
        
        self.create_leaf(path1, value1, branches)
        self.create_leaf(path2, value2, branches)

        return self.save_node(Branch(branches, branch_value))

    def create_leaf(self, path, value, branches):
        if not len(path):
            return
        
        _id = path[0]
        reference = self.save_node(Leaf(path.add_offset(1), value))

        branches[_id] = reference

    def create_extension(self, path, next_node, branches):
        if len(path) == 1:
            # En este caso no es necesario crear un nodo de extensión ya que pasa automático al siguiente
            branches[path[0]] = next_node
        else:
            _id = path[0]
            reference = self.save_node(Extension(path.add_offset(1), next_node))
            branches[_id] = reference

    def save_node(self, node):
        reference = node.into_reference()
        self.nodes[reference] = node.encode()
        return reference
