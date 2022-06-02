import glob
import pandas as pd
import networkx as nx

DATA_BASE_PATH = "/Users/chris/Documents/Research/data/XBlock-ETH"

block_transactions_path = "{}/Block Transactions/0to999999_BlockTransaction/0to999999_BlockTransaction.csv".format(DATA_BASE_PATH)
internal_transactions_path = "{}/Internal Transactions/0to999999_InternalTransaction/0to999999_InternalTransaction.csv".format(DATA_BASE_PATH)
contract_info_path = "{}/Contract Info/0to999999_ContractInfo/0to999999_ContractInfo.csv".format(DATA_BASE_PATH)

NROWS = 100000
root = "0xa1e4380a3b1f749673e270229993ee55f35663b4"
## 
# Create 1-hop subgraphs for each address
# - Combine internal and external transactions for a user
# Record the following txs:
# - Root to wallet (external)
# - Root to contract (internal)
# - Contract to root (internal)
# - Wallet to root (external)
##

# Collect root external transactions
external_txs = glob.glob(block_transactions_path)[0]
external_df = pd.read_csv(external_txs)
print(external_df.shape)

root_to_wallet = external_df[external_df['from']==root]
wallet_to_root = external_df[external_df['to']==root]
print('EXTERNAL TRANSACTIONS: ')
print('Root to wallet: ', root_to_wallet.shape)
print('Wallet to root: ', wallet_to_root.shape)

# Collect root internal transactions
internal_txs = glob.glob(internal_transactions_path)[0]
internal_df = pd.read_csv(internal_txs)
print(internal_df.shape)

root_to_contract = internal_df[internal_df['from']==root]
contract_to_root = internal_df[internal_df['to']==root]
print('INTERNAL TRANSACTIONS: ')
print('Root to contract: ', root_to_contract.shape)
print('Contract to root: ', contract_to_root.shape)

Graphtype = nx.DiGraph()
G = nx.from_pandas_edgelist()













