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

# Construct 2nd-order directed graph
# For each `source` open related csv in 2nd-order directory create new graph
# Then combine network graphs using nx.compose()
# print('Second order nodes of {}:'.format(f1) + '\n')
second_order_files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing second-order nodes/{}/*.csv'.format(current_node))
for f2 in second_order_files:
    df2 = pd.read_csv(f2)
    Graphtype = nx.DiGraph()
    G2 = nx.from_pandas_edgelist(df, source='From', target='To', edge_attr='Value', create_using=Graphtype)
    G = nx.compose(G, G2)

print(G)

