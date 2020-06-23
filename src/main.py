from miner import gSpan
from torch_geometric.datasets import TUDataset

dataset = TUDataset(root='/tmp/AIDS', name='AIDS')

freq_subgraphs = gSpan(dataset, {}, 0.1)
