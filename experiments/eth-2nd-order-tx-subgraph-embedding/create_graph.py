import networkx as nx
import pandas as pd

df = pd.read_csv('/Users/chris/Documents/Research/data/[DATA] 2nd-order transaction network of phishing nodes/Non-phishing/Non-phishing first-order nodes/0x0000000000000000000000000000000000000000.csv')
Graphtype = nx.DiGraph()
G = nx.from_pandas_edgelist(df, source='From', target='To', edge_attr='Value', create_using=Graphtype)

print(G.edges.data())

