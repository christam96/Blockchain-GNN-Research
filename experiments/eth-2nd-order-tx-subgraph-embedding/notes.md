* Create first-order tx graph
* Create second-rder tx graph
* Store tx subgraph somewhere
* Repeat for every address in category (Phishing/Non-phishing)
* Repeat for every address in both categories

Using graph2vec:

Input: List[networkx.classes.graph.Graph]
    - Assert return type of `create_graph()` is 'networkx.classes.graph.Graph'
    - Run through 1st order nodes, create List[networkx.classes.graph.Graph]
    - Instantiate graph2vec
Output: Graph embedding (NumPy array)
