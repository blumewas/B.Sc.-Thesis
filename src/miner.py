import torch as th
import numpy as np
from dfs_code import DFSCode
from torch_geometric.data import Data
from datasets import ReducedDataset

min_occur = 1000

def gSpan(dataset, result):
  # lines 1 - 3
  reduced_dataset, node_relabel_dict, edge_relabel_dict = prepare_dataset(dataset)
  print(node_relabel_dict)
  print(edge_relabel_dict)
  reduced_dataset.wrap_up()
  print(reduced_dataset.loader)
  return result

def prepare_dataset(dataset):
  """Prepares the dataSet of graphs for structure mining
  
    1. Sort the labels of Nodes and Edges
    2. Remove all Nodes/Edges with labels that are in frequent
    3. Relabel the remaining Nodes/Edges with labels from 0-|remaining_labels|
  """
  # Step 1: sort edge and node labels by frequency
  # Init map that holds node_label and respective occurence later
  num_node_features = dataset.num_node_features
  node_label_count = {x: 0 for x in range(num_node_features)}

  # Init map that holds edge_label and respective occurence later
  num_edge_features = dataset.num_edge_features
  edge_label_count = nlabels = {x: 0 for x in range(num_edge_features)}
  for graph_data in dataset:
    # If Graph has node_labels, fill node_label_count dict with (label: count)
    if 'x' in graph_data:
      # Node labels matrix, with shape [node_count,label_count], to indicate that the node x has the label y, value 1 is found at [x, y]
      x = graph_data['x']
      for node in x:
        for i in range(num_node_features):
          if node[i] == 1: # node has label i
            node_label_count[i] = node_label_count[i] + 1
            break
    # If Graph has node_labels, fill node_label_count dict with (label: count)
    if 'edge_attr' in graph_data:
      edge_attr = graph_data['edge_attr'] # Same as node_labels, for edge_labels respectively
      for edge in edge_attr: # edge has label i
        for i in range(num_edge_features):
          if edge[i] == 1:
            edge_label_count[i] = edge_label_count[i] + 1
            break
  
  # sorted results
  node_labels_sorted = sorted(node_label_count.items(),  key=lambda item: item[1], reverse=True)
  edge_labels_sorted = sorted(edge_label_count.items(),  key=lambda item: item[1], reverse=True)
  
  # Step 2.1: detect infrequent labels
  node_labels_after = th.zeros(num_node_features, dtype=th.uint8)
  for l, count in node_labels_sorted:
    if count > min_occur:
      node_labels_after[l] = 1 # set to 1 to indicate that label l should be kept
  nlabel_count_after = th.sum(node_labels_after)

  # Step 3.1: get new labels for relabeling Nodes
  node_relabel_dict = {}
  curr = 0
  for index, label in enumerate(node_labels_after):
    if label == 1:
      node_relabel_dict[index] = curr
      curr += 1

  edge_labels_after = th.zeros(num_edge_features, dtype=th.uint8)
  for l, count in edge_labels_sorted:
    if count > min_occur:
      edge_labels_after[l] = 1
  elabel_count_after = th.sum(edge_labels_after)

  # Relabel Edges
  edge_relabel_dict = {}
  curr = 0
  for index, label in enumerate(edge_labels_after):
    if label == 1:
      edge_relabel_dict[index] = curr
      curr += 1
  
  reduced_dataset = ReducedDataset()
  # Step 2.2, 3.2: Remove infrequent Labels and relabel simultaneously
  for graph_data in dataset:
    new_data = Data()
    if 'x' in graph_data:
      new_x = th.zeros(graph_data.num_nodes, 1) - 1
      x = graph_data['x']
      # store indizes for nodes that have to be removed
      node_remove_list = []
      for i in range(graph_data.num_nodes):
        for j in range(num_node_features):
          # node i has label j and label j is frequent
          if x[i][j] == 1 and node_labels_after[j] == 1:
            new_label = node_relabel_dict[j]
            new_x[i][0] = new_label
            break
          # check if we passed all labels, to determine whether node i has a label afterwards
          if j == num_node_features - 1:
            node_remove_list.append(i)

      # remove Nodes
      for node in node_remove_list[::-1]:
        new_x = th.cat([new_x[:node], new_x[node+1:]])
      new_data.x = new_x
    
    if 'edge_attr' in graph_data:
      new_edge_attr = th.zeros(graph_data.num_edges, 1) - 1
      edge_attr = graph_data['edge_attr']
      # store indizes for edges that have to be removed
      edge_remove_list = []
      # Iterate all edges
      for i in range(graph_data.num_edges):
        for j in range(num_edge_features):
          # node i has label j and label j is frequent
          if edge_attr[i][j] == 1 and edge_labels_after[j] == 1:
            new_label = edge_relabel_dict[j]
            new_edge_attr[i][0] = new_label
            break

          if j == num_edge_features - 1:
            edge_remove_list.append(i)

    edge_index = graph_data.edge_index
    from_nodes = []
    to_nodes = []
    # Iterate all edges by index
    for i in range(graph_data.num_edges):
      if i not in edge_remove_list:
        from_node = edge_index[0][i]
        to_node = edge_index[1][i]
        if from_node not in node_remove_list and to_node not in node_remove_list:
          from_nodes.append(from_node)
          to_nodes.append(to_node)
        else:
          edge_remove_list.append(i)
    new_edges = th.tensor([from_nodes, to_nodes], dtype=th.long)
    new_data.edge_index = new_edges
    # Remove edge_labels
    edge_remove_list = sorted(edge_remove_list)
    for edge in edge_remove_list[::-1]:
      new_edge_attr = th.cat([new_edge_attr[:edge], new_edge_attr[edge+1:]])
    new_data.edge_attr = new_edge_attr

    reduced_dataset.add(new_data)
    
  return reduced_dataset, node_relabel_dict, edge_relabel_dict

def graphset_projection(dataset, result):
  
  # Enumerate frequent one edge graphs
  freq_one_edgers = enumerate_one_edgers(dataset)

  # sort one_edgers in lexicographic order

  # add all frequent_one_edge_graphs to the result
  result = freq_one_edgers

def subgraph_mining(dataset, result, s):
  print('Mining')

def enumerate_one_edgers(dataset):
  dfs_list = []
  for G,l in dataset:
    print('Enumerating')
    for edge in G.edata['_ID']:
      subG = G.edge_subgraph([edge])

      vids = subG.ndata['_ID']
      i = vids[0]
      if vids.len == 1:
        j = i
      else:
        j = vids[1]
      code = DFSCode(i, j, '', '', '')