import rlp
from path import Path
from keccak_hash import keccak_hash
from abc import ABC, abstractmethod


class Node(ABC):

    def __init__(self, type, path=''):
        super().__init__()
        self.type = type
        self.path = path

    @abstractmethod
    def encode(self):
        pass

    @staticmethod
    def decode(encoded_node):
        #print("node", encoded_node)
        node_list = rlp.decode(encoded_node)
        #print("list", node_list)

        if len(node_list) == 17:
            branches = list(map(encode_node_data, node_list[:16]))
            value = node_list[16]
            return Branch(branches, value)

        path, es_hoja = Path.decode_type(node_list[0])
        if es_hoja:
            return Leaf(path, node_list[1])
        reference = encode_node_data(node_list[1])
        return Extension(path, reference)

    def into_reference(self):
        encoded_node = self.encode()
        return keccak_hash(encoded_node)


class Leaf(Node):

    def __init__(self, path, value):
        super().__init__("Leaf", path)
        self.value = value

    def encode(self):
        return rlp.encode([self.path.encode(0), self.value])


class Branch(Node):

    def __init__(self, branches, value):
        super().__init__("Branch")
        self.branches = branches
        self.value = value

    def encode(self):
        branches_ref = list(map(decode_reference, self.branches))
        return rlp.encode(branches_ref + [self.value])


class Extension(Node):

    def __init__(self, path, next_node):
        super().__init__("Extension", path)
        self.next_node = next_node

    def encode(self):
        reference = decode_reference(self.next_node)
        return rlp.encode([self.path.encode(2), reference])


def decode_reference(reference):
    if 0 < len(reference) < 32:
        return rlp.decode(reference)
    
    return reference

def encode_node_data(reference):
    if isinstance(reference, list):
        return rlp.encode(reference)
    
    return reference
