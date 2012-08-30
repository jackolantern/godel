import unittest
from string import ascii_lowercase as abc

from util.bijection import Bijection


class TestBijection(unittest.TestCase):
  def test_mapping(self):
    alphabet = { k : v for k, v in enumerate(abc) }
    bijection = Bijection(alphabet)
    self.assertEqual(bijection.mapping, alphabet)

  def test_inverse(self):
    alphabet = { k : v for k, v in enumerate(abc) }
    inverse_alphabet = { v : k for k, v in enumerate(abc) }
    bijection = Bijection(alphabet)
    self.assertEqual(bijection.inverse, inverse_alphabet)


if __name__ == '__main__':
  unittest.main()
