import collections


class Bijection:
  """
  Creates a one to one mapping.

  Unfortunatly the mappings are mutable, so don't update them unless you want to
  break your bijection.
  """
  def __init__(self, mapping):
    inverse = {}
    for k, v in mapping.items():
      if v in inverse:
        raise ValueError("duplicate key '{0}' found".format(v))
      inverse[v] = k
    self._mapping = dict(mapping)
    self._inverse = inverse

  def __len__(self):
    return len(self.mapping)

  @property
  def mapping(self):
    """
    Return the mapping.
    """
    return self._mapping

  @property
  def inverse(self):
    """
    Return the inverse of the mapping.
    """
    return self._inverse
