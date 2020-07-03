import torch as th
from torch_geometric.data.dataloader import DataLoader

class ReducedDataset:
    def __init__(self):
      self.data_list = []

    def add(self, graph):
      self.data_list.append(graph)

    def __len__(self):
      return len(self.data_list)

    def remove_edge(self, edge):
      """ Remove edge from the dataset """
      new_data = []
      for graph_data in self.data_list:
        edge_index = graph_data['edge_index']
        x = graph_data['x']
        edge_attr = graph_data['edge_attr']

        edge_remove_list = []
        for i in range(graph_data.num_edges):
          from_node = edge_index[0][i]
          to_node = edge_index[1][i]
          edge_label = edge_attr[i][0]
          label_i = x[from_node][0]
          label_j = x[to_node][0]
          
          if edge.edge_label == edge_label and edge.label_i == label_i and edge.label_j == label_j:
            edge_remove_list.append(i)

        new_edge_attr = th.zeros(graph_data.num_edges, 1)
        for i in edge_remove_list[::-1]:
          new_edge_attr = th.cat([new_edge_attr[:i], new_edge_attr[i+1:]])
        graph_data.edge_attr = new_edge_attr

        from_nodes = []
        to_nodes = []
        # Iterate all edges by index
        for i in range(graph_data.num_edges):
          if i not in edge_remove_list:
            from_nodes.append(edge_index[0][i])
            to_nodes.append(edge_index[1][i])

        graph_data.edge_index = th.tensor([from_nodes, to_nodes], dtype=th.long)
        # if the graph has only zero edges remove it
        if graph_data.num_edges > 0:
          new_data.append(graph_data)

      self.data_list = new_data
          