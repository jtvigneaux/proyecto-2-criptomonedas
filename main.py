from MPT import MPT

mpt = MPT({})
mpt.update_trie(b'do', b'verb')
mpt.update_trie(b'dog', b'puppy')
mpt.update_trie(b'doge', b'coin')
mpt.update_trie(b'horse', b'stallion')
#print(mpt.root.hex(), mpt.get_node(mpt.root).branches)
print(mpt.get_node_data(b"horse"))
print(mpt.root.hex(), mpt.get_node(mpt.root))
mpt.update_trie(b'horse', b'otro')
print(mpt.get_node_data(b"horse"))
print(mpt.root.hex(), mpt.get_node(mpt.root))