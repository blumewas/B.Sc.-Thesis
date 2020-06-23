import convert

import networkx.algorithms.isomorphism as iso

def subgraph_isomorphism(graph, sub):
  nm = iso.categorical_node_match('label', -1)
  em = iso.categorical_edge_match('label', -1)
  matcher = iso.GraphMatcher(graph, sub, node_match=nm, edge_match=em)
  return matcher.subgraph_is_isomorphic()

def graph_isomorphism(graph1, graph2):
  nm = iso.categorical_node_match('label', -1)
  em = iso.categorical_edge_match('label', -1)
  matcher = iso.GraphMatcher(graph1, graph2, node_match=nm, edge_match=em)
  return matcher.is_isomorphic()

def is_freq(candidate, dataset, support):
  count = 0
  tested = 0
  for graph_data in dataset:
    if count/len(dataset) >= support:
      return True

    G = convert.geometric_to_nx(graph_data)
    if subgraph_isomorphism(G, candidate):
      count += 1
    tested += 1
  
  return count/len(dataset) >= support

