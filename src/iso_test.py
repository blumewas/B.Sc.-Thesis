import networkx.algorithms.isomorphism as iso

def subgraph_isomorphism(graph, sub):
  nm = iso.numerical_node_match('label', -1)
  em = iso.numerical_edge_match('label', -1)
  matcher = iso.DiGraphMatcher(graph, sub, node_match=nm, edge_match=em)
  return matcher.subgraph_is_isomorphic()

def graph_isomorphism(graph1, graph2):
  nm = iso.numerical_node_match('label', -1)
  em = iso.numerical_edge_match('label', -1)
  matcher = iso.DiGraphMatcher(graph1, graph2, node_match=nm, edge_match=em)
  return matcher.is_isomorphic()
