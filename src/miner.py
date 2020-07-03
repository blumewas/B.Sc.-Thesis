import torch as th
import convert
import iso_test

import networkx as nx

from dfs_code import DFSCode
from torch_geometric.data import Data
from datasets import ReducedDataset

import matplotlib.pyplot as plt

min_occur = 1000

def gSpan(dataset, result, support):
  # lines 1 - 3
  reduced_dataset, node_relabel_dict, edge_relabel_dict = prepare_dataset(dataset)

  # Enumerate frequent one edge graphs. line: 
  freq_one_edgers = enumerate_one_edgers(reduced_dataset.data_list, support)
  # Init result with one edgers in DFS lexicographic order
  freq_one_edgers = sorted(freq_one_edgers)

  for one_edger in freq_one_edgers:
    result.append([one_edger])

  for one_edger in freq_one_edgers:
    start = one_edger # init s with e
    contain_list = get_containing_graphs(start, reduced_dataset.data_list) # get the graphs that contain our one_edger in NetworkX format
    subgraph_mining(contain_list, result, [start], support) # start mining_subprocedure

    # remove all edges with the same DFS_Code (label wise) in all Graphs of the DataSet
    reduced_dataset.remove_edge(one_edger)

    # Check if the count of the remaining Graphs is lower then the support
    remaining_graphs = len(reduced_dataset)
    if remaining_graphs/len(dataset) < support:
      break

  return result

def subgraph_mining(dataset, result, dfs_code, support):
  """ Subprocedure to generate our Graphs recursively
  
    dataset, the dataset to search in
    result, the current result that contains already discovered freq_subgraphs
    dfs_code, the current graph in DFS_Code representation we want to extend
    support, the support threshhold for a graph to be considered as frequent
   """
  # TODO
  # check if dfs_code is min(dfs_code) line 1-2
  if True == False:
    return

  if len(dfs_code) > 1:
    result.append(dfs_code)

  # generate all candidates which start can be extended with, line 4
  candidates = generate_candidates(dfs_code, dataset) # Graphs in NetworkX format

  for c in candidates:
    # check if candidate c is frequent
    if iso_test.is_freq(c, dataset, support, False):
      # call subroutine again with startpoint c
      # TODO: convert c to DFS_Code list
      return subgraph_mining(dataset, result, c, support)

def generate_candidates(dfs_codes, dataset):
  """ Generate all candidates which can expand our current dfs_code """
  candidates = []
  for nx_graph in dataset:
    edges = nx_graph.edges
    nodes = nx_graph.nodes
    # Use DFS to search in nx_graph for current structure
    # TODO
    for from_node, to_node in edges:
      edge_label = edges[from_node, to_node]['label']
      
      # Expand current structures dfs_code

  return candidates

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
          f_new = from_node - get_smaller_removed(from_node, node_remove_list)
          t_new = to_node - get_smaller_removed(to_node, node_remove_list)
          from_nodes.append(f_new)
          to_nodes.append(t_new)
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

def enumerate_one_edgers(dataset, support):
  """Enumerates all one_edgers

    1. Iterate all edges
    2. get labels of from_node, to_node and edge
    3. Create DFSCode and add it to set
  """
  dfs_list = set()
  tested = set()
  for graph_data in dataset:
    edge_index = graph_data.edge_index
    x = graph_data['x']
    edge_attr = graph_data['edge_attr']
    
    for i in range(graph_data.num_edges):
      from_node = edge_index[0][i]
      to_node = edge_index[1][i] # edge_index is two arrays, first is from_node, second is to_node
      edge_label = edge_attr[i][0]
      label_i = x[from_node][0]
      label_j = x[to_node][0]

      code = DFSCode(0, 1, label_i, edge_label, label_j)
      # only consider if the candidate was not already tested
      if code in tested:
        break
      # Create nx.Graph for iso test
      one_edger = nx.Graph()
      one_edger.add_node(from_node, label=label_i)
      one_edger.add_node(to_node, label=label_j)
      one_edger.add_edge(from_node, to_node, label=edge_label)
      # only save the one edger if it is frequent
      if iso_test.is_freq(one_edger, dataset, support):
        code = DFSCode(0, 1, label_i, edge_label, label_j)
        dfs_list.add(code)
      tested.add(code)
  
  return dfs_list

def get_containing_graphs(edge, dataset):
  """ Get all graphs that contain the DFS in networkX foramt """
  dfs_graph = nx.Graph()
  dfs_graph.add_node(edge.i, label=edge.label_i)
  dfs_graph.add_node(edge.j, label=edge.label_j)
  dfs_graph.add_edge(edge.i, edge.j, label=edge.edge_label)

  graph_list = []
  for graph_data in dataset:
    nx_graph = convert.geometric_to_nx(graph_data)
    if iso_test.subgraph_isomorphism(nx_graph, dfs_graph):
      graph_list.append(nx_graph)

  return graph_list

def get_smaller_removed(node, remove_list):
  count = 0
  for r in remove_list:
    if r < node:
      count += 1
  
  return count
