from MPT import MPT

mpt = MPT({})
mpt.update_trie(b'do', b'verb')
mpt.update_trie(b'dog', b'puppy')
mpt.update_trie(b'doge', b'coin')
print(mpt.get_node_data(b"doge"))