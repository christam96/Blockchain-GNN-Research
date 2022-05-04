import glob
import networkx as nx
import pandas as pd

DATA_BASE_PATH = "/Users/chris/Documents/Research/data/2nd-order transaction network of phishing nodes/"

# Construct 1st-order directed graph using only one graph
f1 = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing first-order nodes/0x0000000000000000000000000000000000000000.csv')[0]
root = f1.split('/')[-1].split('.')[0]
df = pd.read_csv(f1)
Graphtype = nx.DiGraph()
G = nx.from_pandas_edgelist(df, source='From', target='To', edge_attr='Value', create_using=Graphtype)
print('Root: ', root)
print('G: ', G)

## Construct 2nd-order directed graph
# Verify graph expansion:
# G'.nodes = G_prev.nodes + G_next.nodes - intersection(G_prev, G_next).nodes
# G'.edges = G_prev.edges + len(G_next.nodes)
count=0
num_incorrect = 0
second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/*.csv'.format(root))
for f2 in second_order_files:
    count += 1
    # Current neighbour of root
    current_neighbour = f2.split('/')[-1].split('.')[0]
    print('# {} [GRAPH EXPANSION] Adding neighbour: {}'.format(count, current_neighbour))

    # Obtain df and filter for txs sent to current neighbour
    df2 = pd.read_csv(f2)
    second_order_nodes = df2[df2['To'] == current_neighbour]

    # Check intersection of nodes with G excluding the neighbour node itself
    existing_nodes = set(G.nodes)
    new_nodes = set(second_order_nodes['From'])
    intersecting_nodes = set(existing_nodes.intersection(new_nodes))
    exp_G_prime_nodes = len(G.nodes) + len(new_nodes) - len(intersecting_nodes)
    exp_G_prime_edges = len(G.edges) + len(new_nodes)

    # Construct graph
    try:
        Graphtype = nx.DiGraph()
        G_next = nx.from_pandas_edgelist(second_order_nodes, source='From', target='To', edge_attr='Value', create_using=Graphtype)
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
        if node_diff > highest_diff: 
            highest_diff = node_diff

print('------------------------------------------')
num_correct = count-num_incorrect
print('Graph Expansion Results: {}/{} ({}%) correct'.format(num_correct, count, num_correct/count*100))
print(G)
print('------------------------------------------')
