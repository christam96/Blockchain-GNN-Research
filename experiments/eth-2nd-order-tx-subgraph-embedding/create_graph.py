import glob
import networkx as nx
import pandas as pd

DATA_BASE_PATH = "/Users/chris/Documents/Research/data/2nd-order transaction network of phishing nodes/"

# Construct 1st-order directed graph using only one graph
f1 = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing first-order nodes/0x0000000000000000000000000000000000000000.csv')[0]
# f1 = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing first-order nodes/0x00a2df284ba5f6428a39dff082ba7ff281852e06.csv')[0]
root = f1.split('/')[-1].split('.')[0]
df = pd.read_csv(f1)
Graphtype = nx.DiGraph()
G = nx.from_pandas_edgelist(df, source='From', target='To', edge_attr='Value', create_using=Graphtype)
print('Root: ', root)
print('G: ', G)

## Construct 2nd-order directed graph
# Filter through addresses:
#   * Filter valid neighbours using df.groupby(['COLUMN']).size() 
#   * link: https://www.geeksforgeeks.org/pandas-groupby-count-occurrences-in-column/
# Verify graph expansion:
# G'.nodes = G_prev.nodes + G_next.nodes - intersection(G_prev, G_next).nodes
# G'.edges = G_prev.edges + G_next.edges - intersection(G_prev, G_next).edges
count=0
num_incorrect = 0
highest_node_diff = 0
highest_edge_diff = 0
second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/*.csv'.format(root))
# second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/0xc3f62567e93661c45b80a0aca87e065802265512.csv'.format(root)) # Correct
# second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/0xc0054cca381f44664bd707ac7fa583fca899e37a.csv'.format(root)) # Incorrect
# second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/0x72a0658eae0a3cbdf92364faca526fd8bbb99ca1.csv'.format(root)) # Incorrect
# second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/0x69b612b2088a75054de71d7ec10dc50d3be94f55.csv'.format(root)) # Incorrect
for f2 in second_order_files:
    count += 1
    # Current neighbour of root
    current_neighbour = f2.split('/')[-1].split('.')[0]
    print('[#{} GRAPH EXPANSION] Adding neighbour: {}'.format(count, current_neighbour))

    # Dataframe of neighbour transactions 
    df2 = pd.read_csv(f2)

    # Verify edges: Remove redundant edges between (G_prev, G_next)
    tx_subset = df2[['From', 'To']]
    tx_tuples = set([tuple(x) for x in tx_subset.to_numpy()])
    intersecting_edges = set(set(G.edges).intersection(tx_tuples))
    new_edges = len(tx_tuples) - len(intersecting_edges)
    exp_G_prime_edges = len(G.edges) + len(tx_tuples) - len(intersecting_edges)

    # Verify nodes: Remove redundant nodes between (G_prev, G_next)
    df2_incoming = set(df2['From'])
    df2_outgoing = set(df2['To'])
    existing_nodes = set(G.nodes)
    new_nodes = set(list(df2_incoming) + list(df2_outgoing))
    intersecting_nodes = set(existing_nodes.intersection(new_nodes))
    exp_G_prime_nodes = len(G.nodes) + len(new_nodes) - len(intersecting_nodes)

    # Construct graph
    try:
        Graphtype = nx.DiGraph()
        G_next = nx.from_pandas_edgelist(df2, source='From', target='To', edge_attr='Value', create_using=Graphtype)
        G_prime = nx.compose(G, G_next)
        assert(len(G_prime.nodes) == exp_G_prime_nodes and len(G_prime.edges) == exp_G_prime_edges)
        print('  ✅ SUCCESS → G\': {}'.format(G_prime))
        G = G_prime
    except Exception as e:
        num_incorrect += 1
        print('  ❌ GRAPH MISMATCH')
        print('{} nodes and {} edges (expected)'.format(exp_G_prime_nodes, exp_G_prime_edges))
        print('{} nodes and {} edges (got)'.format(len(G_prime.nodes), len(G_prime.edges)))
        node_diff = abs(exp_G_prime_nodes - len(G_prime.nodes))
        edge_diff = abs(exp_G_prime_edges - len(G_prime.edges))
        if node_diff > highest_node_diff:
            highest_node_diff = node_diff
        if edge_diff > highest_edge_diff:
            highest_edge_diff = edge_diff

print('------------------------------------------')
num_correct = count-num_incorrect
print('Graph Expansion Results: {}/{} ({}%) correct'.format(num_correct, count, num_correct/count*100))
print(G)
print('Highest node diff: ', highest_node_diff)
print('Highest edge diff: ', highest_edge_diff)
print('------------------------------------------')
