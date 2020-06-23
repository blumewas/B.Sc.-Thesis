""" Helper Class for DFSCode """
class DFSCode:
  def __init__(self, i, j, label_i, edge_label, label_j):
    self.i = i
    self.j = j
    self.label_i = label_i
    self.edge_label = edge_label
    self.label_j = label_j

  def _is_valid_operand(self, other):
    return (hasattr(other, "i") and
      hasattr(other, "j") and
      hasattr(other, "label_i") and
      hasattr(other, "label_j") and
      hasattr(other, "edge_label"))
  
  def __eq__(self, other):
    if not self._is_valid_operand(other):
      return NotImplemented
    return ((self.i, self.j, self.label_i, self.edge_label, self.label_j) ==
      (other.i, other.j, other.label_i, other.edge_label, other.label_j))
  
  def __lt__(self, other):
    if not self._is_valid_operand(other):
      return NotImplemented
    if self.i == other.i:
      return self.j < other.j
    if self.i < self.j:
      return self.j == other.i

  def __hash__(self):
    return hash('i{0} j{1} label_i{2} edge_label{3} label_j{4}'.format(self.i, self.j, self.label_i, self.edge_label, self.label_j)) 
  
  def __str__(self):
    return '({0}, {1}, {2}, {3}, {4})'.format(self.i, self.j, self.label_i, self.edge_label, self.label_j)
