from miner import gSpan
from torch_geometric.datasets import TUDataset

dataset = TUDataset(root='/tmp/AIDS', name='AIDS')

freq_subgraphs = gSpan(dataset, set(), 0.1)

for freq in freq_subgraphs:
    print(freq)
