import rlp
from path import NibblePath
from keccak_hash import keccak_hash
from abc import ABC, abstractmethod


class Node(ABC):

    def __init__(self, path=''):
        super().__init__()
        self.path = path

    @abstractmethod
    def encode(self):
        pass

    def decode(encoded_node):
        pass

    def into_reference(self):
        pass


class Leaf(Node):

    def __init__(self, path, value):
        super().__init__(path)
        self.value = value

    def encode(self):
        pass


class Branch(Node):

    def __init__(self, branches, value):
        super().__init__()
        self.branches = branches
        self.value = value

    def encode(self):
        pass


class Extension(Node):

    def __init__(self, path, value):
        super().__init__(path)
        self.value = value

    def encode(self):
        pass
