import glob
import networkx as nx
import pandas as pd
from karateclub import Graph2Vec
from tqdm import tqdm
import pickle

DATA_BASE_PATH = "/Users/chris/Documents/Research/data/2nd-order transaction network of phishing nodes/"

def create_graph(dataset, root):
    # Construct 1st-order directed graph using only one graph
    f1 = glob.glob(DATA_BASE_PATH + '{}/{} first-order nodes/{}.csv'.format(dataset, dataset, root))[0]
    root = f1.split('/')[-1].split('.')[0]
    df = pd.read_csv(f1)
    Graphtype = nx.DiGraph()
    G = nx.from_pandas_edgelist(df, source='From', target='To', edge_attr='Value', create_using=Graphtype)
    G_start = G
    # print('Root: ', root)
    # print('G: ', G)

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
    c_success = 0
    c_skip = 0
    second_order_files = glob.glob(DATA_BASE_PATH + '{}/{} second-order nodes/{}/*.csv'.format(dataset, dataset, root))
    # Some 2nd-order directories may be empty (e.g., phishing accounts)
    if not second_order_files:
        # print('EMPTY DIRECTORY')
        return nx.empty_graph()
    for f2 in second_order_files:
        count += 1
        # Current neighbour of root
        current_neighbour = f2.split('/')[-1].split('.')[0]
        # print('[#{} GRAPH EXPANSION] Adding neighbour: {}'.format(count, current_neighbour))

        # Dataframe of neighbour transactions 
        df2 = pd.read_csv(f2)

        ## Filter through valid addresses
        # Count number of transactions with each neighbour
        count_from = df2.groupby('From').size()
        count_to = df2.groupby('To').size()
        count_txs = count_from.add(count_to, fill_value=0).drop(current_neighbour)
        # Only keep neighbours with more than 10 and less than 300 transactions
        bool_filter = count_txs.apply(lambda x : x >= 10 and x <= 300)
        valid_addresses = pd.DataFrame(bool_filter[bool_filter==True])
        if valid_addresses.empty == True: 
            # print('  ⏩ SKIPPING: Empty DataFrame')
            c_skip += 1
            continue
        valid_addresses.reset_index(inplace=True)
        valid_addresses = valid_addresses.iloc[:,0].tolist()
        # Remove all other neighbours from subgraph 
        df2 = df2[(df2['From'].isin(valid_addresses)) | (df2['To'].isin(valid_addresses))]

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
            # print('  ✅ SUCCESS → G\': {}'.format(G_prime))
            c_success += 1
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

    # print('------------------------------------------')
    # num_correct = count-num_incorrect
    # print('Graph Expansion Results: {}/{} ({}%) correct'.format(num_correct, count, num_correct/count*100))
    # print('Succeeded: {} | Skipped: {} | ({}/{})'.format(c_success, c_skip, c_success+c_skip, count))
    # print('Initial graph: \t{}'.format(G_start))
    # print('Final graph: \t{}'.format(G))
    # print('Highest node diff: ', highest_node_diff)
    # print('Highest edge diff: ', highest_edge_diff)
    # print('------------------------------------------')
    return G


# create_graph('Non-phishing', '0x0000000000000000000000000000000000000000')
# create_graph('Non-phishing', '0x00a2df284ba5f6428a39dff082ba7ff281852e06')
# create_graph('Non-phishing', '0x0a17c49ca376b47b64c743b3cd6a0b795599141d')
# create_graph('Non-phishing', '0x0a34b447d8a19693ffb41b083f86b09dd90109d8')

# create_graph('Phishing', '0x0a0ba956038d4a66002d612648332b9c4ab7646c')
# create_graph('Phishing', '0x0a3afd85b3b4dbab37906030287de6fc70a83b92')
# create_graph('Phishing', '0x0a4a2413d7c604647c7788fd3564b3c54fe06763')
# create_graph('Phishing', '0x0a9f58ee19a7131ed031ea66a032c05c7efe965a')

# Create list of subgraphs
first_order_files = glob.glob(DATA_BASE_PATH + 'Phishing/Phishing first-order nodes/*')
graph_l = []
for f in tqdm(first_order_files, desc="Loading..."):
    root = f.split('/')[-1].split('.')[0]
    G = create_graph('Phishing', root)
    graph_l.append(nx.convert_node_labels_to_integers(G, first_label=0, ordering='default'))

print(len(graph_l))

model = Graph2Vec()
fit = model.fit(graph_l)
embedding = model.get_embedding()
print(embedding.shape)
