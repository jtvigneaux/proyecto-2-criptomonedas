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
            return None

        hash_key = keccak_hash(key)
        print(hash_key)

    def update_trie(self, key, value):
        hash_key = keccak_hash(key)

        node_path = Path(hash_key)
        result = self.update(self.root, node_path, value)

        self.root = result

    # Métodos que sólo se llaman dentro de la clase
    def get_node(ref):
    	encode_node = self.nodes[ref]
    	return Node.decode(encode_node)

    def update(self, node_ref, path, value):
        # Si no hay un nodo de referencia
        if not node_ref:
            # Guardar un nuevo nodo hoja y retornarlo
            return self.save_node(Leaf(path, value))

       node = get_node(node_ref)

       if isinstance(node, Leaf):
       	# Está la opción de que se este actualizando un nodo hoja o que se este creando
       	if node.path == path:
       		node.value = value
       		return self.save_node(node)

       	# Encontrar ruta comun
       	common_path = path.common_path(node.path)

    def save_node(self, node):
        reference = node.into_reference()
        self.nodes[reference] = node.encode()
        return reference
