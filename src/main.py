from miner import gSpan
from torch_geometric.datasets import TUDataset

dataset = TUDataset(root='/tmp/Tox21_p53_testing', name='Tox21_p53_testing')

freq_subgraphs = gSpan(dataset, {})
