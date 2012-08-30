"""
Basic arithmetical functions and utilities.
"""

def prod(iterable):
  """
  Returns the product of the elements of iterable.
  """
  product = 1
  for n in iterable:
    product *= n
  return product
