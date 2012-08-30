"""
Basic number theory functions and tools.
"""

from math import sqrt


def sieve(n):
  """
  Returns all primes smaller than the argument "n".
  """
  if n < 2: return []  

  lng = int((n / 2) - 1 + n % 2)  ## Remove even numbers.
  sieve = [True] * (lng + 1)  

  for i in range(int(sqrt(n)) >> 1):  
    if not sieve[i]: continue
    ## Unmark all multiples of i, starting at i**2  
    for j in range( (i * (i + 3) << 1) + 3, lng, (i << 1) + 3):  
      sieve[j] = False

  primes = [2] + [(i << 1) + 3 for i in range(lng) if sieve[i]]
  return primes


def factor(n):
  """
  Returns an array of the prime factors of the argument "n" from smallest
  to largest.
  """
  factor = 2
  factors = []
  while factor <= n:
    if n % factor == 0:
      n //= factor
      factors.append(factor)
    else:
      factor += 1
  return factors
