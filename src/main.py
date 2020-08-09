from miner import gSpan
from torch_geometric.datasets import TUDataset

# dataset = TUDataset(root='/tmp/AIDS', name='AIDS')
dataset = TUDataset(root='/tmp/PTC_FM', name='PTC_FM')

freq_subgraphs = gSpan(dataset, [], 0.05)

# for freq in freq_subgraphs:
#   print('new Frequent sub_graph')
#   for f in freq:
#     print(f)

print(len(freq_subgraphs))
