from karateclub import Graph2Vec
import pickle

unpickle = open('p-subgraphs.pickle', 'rb')
subgraphs = pickle.load(unpickle)
print(len(subgraphs))

model = Graph2Vec(wl_iterations=20, dimensions=256)
fit = model.fit(subgraphs)
embedding = model.get_embedding()
print(embedding.shape)

with open('p-embeddings.pickle', 'wb') as fh:
    pickle.dump(embedding, fh)
