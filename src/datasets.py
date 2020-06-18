import torch as th
from torch_geometric.data.dataloader import DataLoader

class ReducedDataset:
    def __init__(self):
      self.data_list = []

    def add(self, graph):
      self.data_list.append(graph)

    def wrap_up(self):
      self.loader = DataLoader(self.data_list)

    def __len__(self):
      return len(self.data_list)