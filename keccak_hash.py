from Crypto.Hash import keccak

import rlp


def keccak_hash(hash_data):
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(hash_data)
    return keccak_hash.digest()


if __name__ == '__main__':
    print(rlp.decode(rlp.encode("holaasg")),
          keccak_hash(rlp.encode("holaasg")))
