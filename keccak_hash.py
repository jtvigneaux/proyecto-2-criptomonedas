from Crypto.Hash import keccak

import rlp


def keccak_hash(hash_data):
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(hash_data)
    return keccak_hash.digest()


if __name__ == '__main__':
    print(1, len(keccak_hash(b"holaasg")), keccak_hash(b"holaasg"))
    print(2, len(keccak_hash(rlp.encode("holaasg"))), keccak_hash(rlp.encode("holaasg")))
    for i in range(1, 32):
        par = i % 2 == 0
        if not par:
            print(keccak_hash(b"holaasg")[i] & 0x0F)
        else:
            print(keccak_hash(b"holaasg")[i] >> 4)
