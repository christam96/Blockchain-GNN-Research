# Notes


# Outline
- Research mindmap


# Research mindmap
Tracking research ideas and opportunities.

- Dataset creation: Create datasets for specific Web3 applications?
  - Marketplaces
  - NFTs
  - Web3 IDs
  - Cross-chain?

- Literature review: Other problems beyond phishing detection?
  - Some nice ideas discussed in 'Understanding Ethereum via Graph Analysis' by T. Chen et al.

- Capture network effects in response to stimuli
  - Temporal analysis of subgraph effects
  - E.x. NFT launch at timestep T, network effects at timestep T+1,T+2,..T+N
  - Embedded representation at each timestep
  - Do similar representations display similar network patterns?

- 'Tag' contract, deploy in network and observe network effects

# Capturing Network Effects
- Quantifying similarity of new users using evolution of transaction subgraph
  - Inuition: Know more about a user the more transactions they make
  - P(next transaction | subgraph)
    - Problem: Not much data to train on
    - Solution: Similarity of users. Find embedding at timestep T that is closest to user embedding.
    - Example:
    1. Minimum threshold of X transactions in user subgraph (S_u)
    2. Embed S_u, E_s_u

# Similarity of transaction subgraphs
- Do similar embeddings represent similar transaction patterns? 
- Similar transactions patterns i.e. same wallets/accounts
- Obtain 1-hop transaction subgraphs for user
- Filter criteria (e.g., 30 < number of user txs < 300)
- Embed transaction subgraph
- Cluster embeddings using k-means clustering
