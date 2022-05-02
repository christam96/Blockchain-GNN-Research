import networkx as nx
import pandas as pd

# l1 - Df edges
df = pd.read_csv('/Users/chris/Documents/Research/data/[DATA] 2nd-order transaction network of phishing nodes/Non-phishing/Non-phishing first-order nodes/0x0000000000000000000000000000000000000000.csv')
l = []

# Sum total 'Values' for each unique address
unique_addresses = df['From'].unique()
for i in range(len(unique_addresses)):
    sum = str(df[df['From']==unique_addresses[i]]['Value'].sum())
    rec = {'From': unique_addresses[i], 'Value': sum}
    l.append(rec)

# l2 - Graph edges
df = pd.read_csv('/Users/chris/Documents/Research/data/[DATA] 2nd-order transaction network of phishing nodes/Non-phishing/Non-phishing first-order nodes/0x0000000000000000000000000000000000000000.csv')
Graphtype = nx.DiGraph()
G = nx.from_pandas_edgelist(df, source='From', target='To', edge_attr='Value', create_using=Graphtype)

l2 = []
for i in G.edges.data():
    val = str(i[-1]).split(' ')[1][:-1]
    rec = {'From': i[0], 'Value': val}
    l2.append(rec)

no_match = 0
for i in range(len(l)):
    if l[i] != l2[i]:
        no_match += 1
    
print(no_match)
