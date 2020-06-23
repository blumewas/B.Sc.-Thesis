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
    is_self_backward = self.i > self.j
    is_other_forward = other.i < other.j
    # check if this is backward edge and other is forward
    if is_self_backward and is_other_forward:
      return True
    # Case both are backward edges
    if is_self_backward and (not is_other_forward):
      if self.j == other.j:
        return self.edge_label < other.edge_label
      return self.j < other.j
    # Case both forward
    if (not is_self_backward) and is_other_forward:
      if self.i == other.i and self.label_i == other.label_i and self.edge_label == other.edge_label:
        return self.label_j < other.label_j
      if self.i == other.i and self.label_i == other.label_i:
        return self.edge_label < other.edge_label
      if self.i == other.i:
        return self.label_i < other.label_i
      return self.i < other.i

  def __hash__(self):
    return hash('i{0} j{1} label_i{2} edge_label{3} label_j{4}'.format(self.i, self.j, self.label_i, self.edge_label, self.label_j)) 
  
  def __str__(self):
    return '({0}, {1}, {2}, {3}, {4})'.format(self.i, self.j, self.label_i, self.edge_label, self.label_j)
