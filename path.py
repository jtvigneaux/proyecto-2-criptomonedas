

class Path:

    def __init__(self, path, offset=0):
        self.path = path
        self.offset = offset

    def __len__(self):
        return len(self.path) * 2 - self.offset

    def __repr__(self):
        return "<Path: Ruta: 0x{}, Offset: {}>".format(self.path.hex(), self.offset)

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for i in range(len(self)):
            if self[i] != other[i]:
                return False

        return True

    def __getitem__(self, key):
        _id = key + self.offset

        byte_id = _id // 2
        nibble_id = _id % 2

        _byte = self.path[byte_id]

        nibble = _byte >> 4 if nibble_id == 0 else _byte & 0x0F

        return nibble

    @staticmethod
    def create_new_path(path, length):
        data = []

        is_odd_len = length % 2 == 1
        pos = 0

        if is_odd_len:
            data.append(path.at(pos))
            pos += 1

        while pos < length:
            data.append(path.at(pos) * 16 + path.at(pos + 1))
            pos += 2

        offset = 1 if is_odd_len else 0

        return Path(data, offset)

    @staticmethod
    def decode_type(path):
        es_impar = path[0] & 0x10 == 0x10
        es_hoja = path[0] & 0x20 == 0x20

        offset = 1 if es_impar else 2

        return Path(path, offset), es_hoja

    def common_path(self, node_path):
        length = min(len(self), len(node_path))
        common_path_len = 0
        for i in range(length):
            if self[i] != node_path[i]:
                break
            common_path_len += 1

        return Path.create_new_path(self, common_path_len)

    def add_offset(self, number):
        self.offset += number
        return self

    def is_prefix(self, other):
        if len(self) < len(other):
            return False
        
        for i in range(len(other)):
            if self[i] != other[i]:
                return False

        return True

    def encode(self, node_type):
        # node_type = 0 para leaf, 1 para branch, 2 para extension
        output = []
        
        length = len(self)
        es_impar = length % 2 == 1

        prefix = 0x10 + self[0] if es_impar else 0x00
        prefix += 0x20 if node_type == 0 else 0x00

        output.append(prefix)

        position = length % 2
        for pos in range(position, length, 2):
            byte = self[pos] * 16 + self[pos + 1]
            output.append(byte)

        return bytes(output)
