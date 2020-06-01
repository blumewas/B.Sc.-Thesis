import torch as th
import numpy as np
from dgl import DGLGraph
from dgl.data import TUDataset

min_occur = 5000

def graphset_projection(dataset, result):
  dataset = TUDataset(dataset)

  # sort edge and node labels by frequency
  vlabels = {}
  elabels = {}
  for G,l in dataset:
    if 'node_labels' in G.ndata:
      vertice_labels = G.ndata['node_labels']
      unique_labels, counts = th.unique(vertice_labels, sorted=True, return_counts=True)
      vlabels = add_results(unique_labels, counts, vlabels)
    
    if 'edge_labels' in G.edata:
      edge_labels = G.edata['edge_labels']
      unique_labels, counts = th.unique(edge_labels, sorted=True, return_counts=True)
      elabels = add_results(unique_labels, counts, elabels)
    
  vlabels_sorted = sorted(vlabels.items(),  key=lambda item: item[1], reverse=True)
  elabels_sorted = sorted(elabels.items(),  key=lambda item: item[1], reverse=True)
  
  # remove infrequent vertices and edges
  for G,l in dataset:
    if 'node_labels' in G.ndata:
      totrim = list()
      vls = G.ndata['node_labels'].numpy()
      for v in G.nodes():
        curr_label = vls[v]
        if vlabels[curr_label] < min_occur:
          totrim.append(v) # add node Id/index to remove
      G.remove_nodes(totrim)

    if 'edge_labels' in G.edata:
      totrim = list()
      els = G.edata['edge_labels'].numpy()
      for i in range(0, els.size):
        curr_label = els[i]
        if elabels[curr_label] < min_occur:
          totrim.append(i) # add edge index to remove
      G.remove_edges(totrim)

  # relabel remaining

  # Enumerate frequent one edge graphs
  freq_one_edgers = enumerate_one_edgers()

  # sort one_edgers in lexicographic order

  # add all frequent_one_edge_graphs to the result
  result = freq_one_edgers

def subgraph_mining(dataset, result, s):
  print('Mining')

def enumerate_one_edgers():
  print('Enumerating')

def add_results(labels, counts, result):
  npl = labels.numpy()
  npc = counts.numpy() # convert for operations to numpy arrays
  
  for x in npl:
    i = np.where(npl == x)[0][0]
    
    if x in result:
      result[x] += npc[i]
    else:
      result[x] = npc[i]
  return result
