

class Path:

    def __init__(self, path, offset=0):
        self.path = path
        self.offset = offset

    def __len__(self):
        return len(self.path) * 2 - self.offset

    def __repr__(self):
        return "<NibblePath: Data: 0x{}, Offset: {}>".format(self.path.hex(), self.offset)

    def __str__(self):
        return '<Hex 0x{} | Raw {}>'.format(self.path.hex(), self.path)

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for i in range(len(self)):
            if self.at(i) != other.at(i):
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

    def common_path(self, node_path):
        length = min(len(self), len(node_path))
        common_path_len = 0
        for i in range(length):
            if self[i] != node_path[i]:
                break
            common_path_len += 1

        return Path.create_new_path(self, common_path_len)
