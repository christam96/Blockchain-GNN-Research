from karateclub import Graph2Vec
import pickle

subgraphs = ['p', 'np']
for sg in subgraphs:
    unpickle = open('{}-subgraphs.pickle'.format(sg), 'rb')
    subgraphs = pickle.load(unpickle)
    print(len(subgraphs))

    model = Graph2Vec(wl_iterations=10, dimensions=256)
    fit = model.fit(subgraphs)
    embedding = model.get_embedding()
    print(embedding.shape)

    with open('{}-embeddings.pickle'.format(sg), 'wb') as fh:
        pickle.dump(embedding, fh)
