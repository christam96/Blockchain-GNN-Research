import glob
import networkx as nx
import pandas as pd

DATA_BASE_PATH = "/Users/chris/Documents/Research/data/2nd-order transaction network of phishing nodes/"
# first_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing first-order nodes/*.csv')
# for f1 in first_order_files:

# Construct 1st-order directed graph using only one graph
f1 = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing first-order nodes/0x0000000000000000000000000000000000000000.csv')[0]
current_node = f1.split('/')[-1].split('.')[0]
df = pd.read_csv(f1)
Graphtype = nx.DiGraph()
G = nx.from_pandas_edgelist(df, source='From', target='To', edge_attr='Value', create_using=Graphtype)
print('Root: ', current_node)
print('G: ', G)

## Construct 2nd-order directed graph
# For each neighbour, open related csv in 2nd-order directory and create new graph
# Then combine network graphs using nx.compose()
#
## Verify graph expansion:
# G'.nodes = G_prev.nodes + G_next.nodes - intersection(G_prev, G_next).nodes
# G'.edges = G_prev.edges + len(G_next.nodes)

# second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/0x00b4bf84e603e491cbee8c387d8d0a017953e12b.csv'.format(current_node))
second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/0xefa34650a61367f3303e9298ae03a130b5613da2.csv'.format(current_node))
for f2 in second_order_files:
    # Current neighbour of root
    current_neighbour = f2.split('/')[-1].split('.')[0]
    print('[GRAPH EXPANSION] Adding neighbour: {}'.format(current_neighbour))

    # Obtain df and filter for txs sent to current neighbour
    df2 = pd.read_csv(f2)
    second_order_nodes = df2[df2['To'] == current_neighbour]

    # Check intersection of nodes with G excluding the neighbour node itself
    intersect_df = pd.merge(df['From'], df2['From'], how='inner')
    intersect_df.drop(intersect_df[intersect_df['From']==current_neighbour].index, inplace=True)
    exp_G_prime_nodes = len(G.nodes) + len(pd.unique(second_order_nodes['From'])) - len(pd.unique(intersect_df['From']))
    exp_G_prime_edges = len(G.edges) + len(pd.unique(second_order_nodes['From']))

    # Construct graph
    try:
        Graphtype = nx.DiGraph()
        G_next = nx.from_pandas_edgelist(second_order_nodes, source='From', target='To', edge_attr='Value', create_using=Graphtype)
        G_prime = nx.compose(G, G_next)
        assert(len(G_prime.nodes) == exp_G_prime_nodes and len(G_prime.edges) == exp_G_prime_edges)
        print('  ✅ SUCCESS → G\': {}'.format(G_prime))
    except Exception as e:
        print('  ❌ GRAPH MISMATCH')
