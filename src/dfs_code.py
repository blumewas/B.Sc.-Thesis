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
    return ((self.lastname.lower(), self.firstname.lower()) ==
      (other.lastname.lower(), other.firstname.lower()))
  
  def __lt__(self, other):
    if not self._is_valid_operand(other):
      return NotImplemented
    if self.i == other.i:
      return self.j < other.j
    if self.i < self.j:
      return self.j == other.i
    