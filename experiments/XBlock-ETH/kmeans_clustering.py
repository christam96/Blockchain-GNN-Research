from sklearn.cluster import KMeans
import pickle

##### Cluster subgraph embeddings using k-means clustering
# In: 2D matrix of subgraphs embeddings
# Compute: Cluster using k-means clustering
# Out: Dictionary containing {wallet address : cluster label}
#####

# Recover subgraph embeddings from pickle
unpickle = open('XBlock-embeddings-{}.pickle'.format('0to999999'), 'rb')
embeddings = pickle.load(unpickle)
print(embeddings.shape)

# Recover subgraph address book from pickle
unpickle = open('subgraphs-addressbook-{}.pickle'.format('0to999999'), 'rb')
address_book = pickle.load(unpickle)
print(address_book)

# Compute k-means clustering of subgraph embeddings
kmeans = KMeans(n_clusters=3, random_state=0).fit(embeddings)
print(kmeans)
print('Labels: ', kmeans.labels_)

# Create dict of {wallet address : cluster label}
address_labels = dict(zip(address_book, kmeans.labels_))
print(address_labels)
