import glob
import pandas as pd
import networkx as nx

DATA_BASE_PATH = "/Users/chris/Documents/Research/data/XBlock-ETH"
NROWS = 100000

block_transactions_path = "{}/Block Transactions/0to999999_BlockTransaction/0to999999_BlockTransaction.csv".format(DATA_BASE_PATH)
internal_transactions_path = "{}/Internal Transactions/0to999999_InternalTransaction/0to999999_InternalTransaction.csv".format(DATA_BASE_PATH)
contract_info_path = "{}/Contract Info/0to999999_ContractInfo/0to999999_ContractInfo.csv".format(DATA_BASE_PATH)

root = "0xa1e4380a3b1f749673e270229993ee55f35663b4"

## 
# Create 1-hop subgraphs for each wallet 
# - Root to wallet (external)
# - Root to contract (internal)
# - Contract to root (internal)
# - Wallet to root (external)
##

# Collect XBlock-ETH transaction data
external_txs = glob.glob(block_transactions_path)[0]
internal_txs = glob.glob(internal_transactions_path)[0]

# Create transaction dataframes
external_df = pd.read_csv(external_txs, nrows=NROWS)
external_df = external_df[external_df['isError']=='None']
internal_df = pd.read_csv(internal_txs, nrows=NROWS)
internal_df = internal_df[internal_df['isError']=='None']
print(external_df.shape)
print(internal_df.shape)

# Distinct wallet addresses
from_wallets = set(external_df['from'])
to_wallets = set(external_df['from'])
wallets = from_wallets.union(to_wallets)
print('# distinct wallets: ', len(wallets))


print('-----------------------------')


subgraphs = []
for root in wallets:

    # Outbound txs from root
    from_root = external_df[external_df['from']==root]
    root_to_wallet = from_root[from_root['toIsContract']==0]
    root_to_contract = from_root[from_root['toIsContract']==1]
    print('OUTBOUND TRANSACTIONS: ')
    print('Root to wallet: ', root_to_wallet.shape)
    print('Root to contract: ', root_to_contract.shape)

    # Inbound txs to root
    wallet_to_root = external_df[external_df['to']==root]
    contract_to_root = internal_df[internal_df['to']==root]
    print('INTERNAL TRANSACTIONS: ')
    print('Wallet to root: ',wallet_to_root.shape)
    print('Contract to root: ', contract_to_root.shape)


    print('-----------------------------')


    # Outbound graphs
    G_r2w = nx.from_pandas_edgelist(root_to_wallet, source='from', target='to', edge_attr='value', create_using=nx.DiGraph())
    G_r2c = nx.from_pandas_edgelist(root_to_contract, source='from', target='to', edge_attr='value', create_using=nx.DiGraph())
    print('OUTBOUND GRAPHS: ')
    print('Root to wallet: ', G_r2w.nodes)
    print('Root to contract: ', G_r2c.nodes)

    # Inbound graphs
    G_w2r = nx.from_pandas_edgelist(wallet_to_root, source='from', target='to', edge_attr='value', create_using=nx.DiGraph())
    G_c2r = nx.from_pandas_edgelist(contract_to_root, source='from', target='to', edge_attr='value', create_using=nx.DiGraph())
    print('INBOUND GRAPHS: ')
    print('Wallet to root: ', G_w2r.nodes)
    print('Contract to root: ', G_c2r.nodes)


    print('-----------------------------')


    # Create subgraph
    G = nx.compose_all([G_r2w, G_r2c, G_w2r, G_c2r])
    print('TX SUBGRAPH: ')
    print(G)
    print('Nodes: ', G.nodes)
    print('Edges: ', G.edges)

    # Append G to subgraphs list
    subgraphs.append(G)

print(len(subgraphs))
