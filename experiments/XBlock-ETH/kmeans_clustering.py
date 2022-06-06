from sklearn.cluster import KMeans
import pickle
import networkx as nx

##### Cluster subgraph embeddings using k-means clustering
# In: 2D matrix of subgraphs embeddings
# Compute: Cluster using k-means clustering
# Out: Dictionary containing {wallet address : cluster label}
#####

# Recover subgraph embeddings from pickle
unpickle = open('XBlock-embeddings-{}.pickle'.format('0to999999'), 'rb')
embeddings = pickle.load(unpickle)
print(embeddings.shape)

# # Recover subgraph address book from pickle
# unpickle = open('subgraphs-addressbook-{}.pickle'.format('0to999999'), 'rb')
# address_book = pickle.load(unpickle)
# print(address_book)

# Compute k-means clustering of subgraph embeddings
kmeans = KMeans(n_clusters=5, random_state=0, n_init=20).fit(embeddings)
print(kmeans)
print('Labels: ', kmeans.labels_)

# # Create dict of {wallet address : cluster label}
# address_labels = dict(zip(address_book, kmeans.labels_))
# print(address_labels)

# Use subgraphs to check similarities within same clusters
unpickle = open('XBlock-subgraphs-{}.pickle'.format('0to999999'), 'rb')
subgraphs = pickle.load(unpickle)

# Get indices for each label
g0_indices = [i for i, value in enumerate(kmeans.labels_) if value == 0]
g1_indices = [i for i, value in enumerate(kmeans.labels_) if value == 1]
g2_indices = [i for i, value in enumerate(kmeans.labels_) if value == 2]
g3_indices = [i for i, value in enumerate(kmeans.labels_) if value == 3]
g4_indices = [i for i, value in enumerate(kmeans.labels_) if value == 4]

print('---------------------------------')
print('GROUP 0')
for idx in g0_indices:
    print(subgraphs[idx])
    # print(subgraphs[idx].edges())

print('---------------------------------')
print('GROUP 1')
for idx in g1_indices:
    print(subgraphs[idx])
    # print(subgraphs[idx].edges.data("value"))

print('---------------------------------')
print('GROUP 2')
for idx in g2_indices:
    print(subgraphs[idx])

print('---------------------------------')
print('GROUP 3')
for idx in g2_indices:
    print(subgraphs[idx])

print('---------------------------------')
print('GROUP 4')
for idx in g2_indices:
    print(subgraphs[idx])
