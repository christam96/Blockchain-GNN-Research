###################
# Identity Inference on Blockchain using Graph Neural Network
#
# OUTLINE
# | General Notes
####################

# General Notes
- Authors propose I^2BGNN, an end-to-end GNN model which accepts subgraphs as input and learns an entire graph representation to predict subgraph labels

- Prediction is binary classification for identity inference (phisher or non-phiser)

- Authors argue that node classiciation on blockchain data results in predicting on large networks with millions of nodes
  - Since node classification is prohibitively expensive, transforming problem into graph classification saves on less compute time and memory consumption <- **'This intuition makes sense to me but do we have evidence to support this?'

- I^2BGNN architecture:
  1) A_v(A_t) and X are captured from subgraph extraction and sent to GCN
  2) Max-pooling layer compresses the aggregated node representations to obtain the whole graph representation
  3) Graph representation used to predict subgraph labels

  Where,
  A = {(a_i,y_i)|i=1,2,...n_a}, set of n_a labeled accounts
  A_v = Account subgraph transaction volume
  A_t = Account subgraph transaction frequency

  **'Revise section for correctness'

- Authors achieve SOTA results on EOSG and ETHG datasets, beating Graph2vec, SF, Netlsd and FGSD approaches


