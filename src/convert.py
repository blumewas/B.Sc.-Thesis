import networkx as nx

def geometric_to_nx(graph_data):
  G = nx.Graph()
  x = graph_data['x'].numpy()
  edge_attr = graph_data['edge_attr'].numpy() # Same as node_labels, for edge_labels respectively
  edge_index = graph_data.edge_index.numpy()

  for i in range(len(x)):
    G.add_node(i, label=x[i][0])
  
  for i in range(len(edge_attr)):
    G.add_edge(edge_index[0][i], edge_index[1][i], label=edge_attr[i][0])
  
  return G

def geometric_to_nx_dataset(dataset):
  graph_list = set()
  for graph_data in dataset:
    nx_graph = convert.geometric_to_nx(graph_data)
    graph_list.add(nx_graph)
  
  return graph_list

def dfs_to_nx(code_list):
  G = nx.Graph()
  for dfs_code in code_list:
    G.add_node(dfs_code.i, label=dfs_code.label_i)
    G.add_node(dfs_code.j, label=dfs_code.label_j)
    G.add_edge(dfs_code.i, dfs_code.j, label=dfs_code.edge_label)

  return G
