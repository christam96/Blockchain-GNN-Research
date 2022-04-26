import glob
import networkx as nx
import pandas as pd

# List of all files in 1st-order node directory
DATA_BASE_PATH = "/Users/chris/Documents/Research/data/2nd-order transaction network of phishing nodes/"
files = glob.glob(DATA_BASE_PATH + 'Non-phishing/Non-phishing first-order nodes/*.csv')

print(G.edges.data())

