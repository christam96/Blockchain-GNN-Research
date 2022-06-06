from karateclub import Graph2Vec
import pickle

##### Create subgraph embeddings
# In: List of transaction subgraphs
# Compute: Use embedding model of choice
#    * graph2vec
# Out: Subgraph embeddings
#####

unpickle = open('XBlock-subgraphs-{}.pickle'.format('0to999999'), 'rb')
subgraphs = pickle.load(unpickle)
print(len(subgraphs))

model = Graph2Vec(wl_iterations=10, dimensions=256)
fit = model.fit(subgraphs)
embedding = model.get_embedding()
print(embedding.shape)

with open('XBlock-embeddings-{}.pickle'.format('0to999999'), 'wb') as fh:
    pickle.dump(embedding, fh)
