#!/usr/bin/python
# This Python file uses the following encoding: utf-8

"""
Encode and decode "Gödel Numbers" as described in the book "Gödel's Proof" by
Ernest Nagel and James R. Newman.
"""

from re import Scanner
from itertools import groupby, takewhile

from util.ntheory import sieve, factor
from util.bijection import Bijection
from util.arithmetic import prod

## Configuration of the program can be accomplished by modifying the following 
## global variables.

## UPPERBOUND_OF_PRIMES determines how many primes to calculate when the program
## starts.  A larger number means that larger expressions can be encoded, but
## also means a longer startup time, and more memory use.
## Specifically, an expression can only have as many terms as there are primes 
## below UPPERBOUND_OF_PRIMES.  There are approximately sqrt(n)/ln(sqrt(n))
## primes below the number sqrt(n).
UPPERBOUND_OF_PRIMES = 10000

## Once the variables are exhausted, they will be reused, with the *character*
## in TICK appended to them.  For example if TICK='`' and
## NUMERICAL_VARIABLES='x','y','z' than after the variables x, y, z were used
## the next variable would be x` then y` then z` and then x`` and so on.
TICK = '`'

## There are three variable types, numerical, sentential, and predicate.  Their
## contents must not overlap.
NUMERICAL_VARIABLES = 'x', 'y', 'z'
SENTNTIAL_VARIABLES = 'p', 'q', 'r'
PREDICATE_VARIABLES = 'P', 'Q', 'R'
ALL_VARIABLES = NUMERICAL_VARIABLES + SENTNTIAL_VARIABLES + PREDICATE_VARIABLES

## These are the constant signs used in the text, (page 70 in the 2001 edition)
## they may be changed to more convenient values simply by changing them below.
CONSTANT_SIGNS = Bijection({
  '~' : 1,
  '∨' : 2,
  '⊃' : 3,
  '∃' : 4,
  '=' : 5,
  '0' : 6,
  's' : 7,
  '(' : 8,
  ')' : 9,
  ',' : 10,
  '+' : 11,
  '×' : 12
})
## End of configuration section

## Calculate all of the primes below UPPERBOUND_OF_PRIMES
PRIME = sieve(UPPERBOUND_OF_PRIMES)

## For variablle identifiers we are only interested in primes above the highest
## number given as a value in CONSTANT_SIGNS.
MAX = max(CONSTANT_SIGNS.mapping.values())
PRIME_OFFSET = len(list(takewhile(lambda x: x < MAX, PRIME)))


class LexicalException(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


class Lexer:
  """
  A simple lexer which simply wraps and configures re.Scanner.

  Unfortunately this method forces us to tokenize the complete input before
  beginning the encoding.  This works for many strings, but is infeasible for
  some use cases.  If you wish to parse *very* large strings, you may wish to
  use another lexer.
  """
  constant_type = "C"
  numerical_type = "N"
  sentntial_type = "S"
  predicate_type = "P"

  def __init__(self):
    self.constant_signs = self.match_any(CONSTANT_SIGNS.mapping.keys())
    self.numerical_variables = self.match_any_with_ticks(NUMERICAL_VARIABLES)
    self.sentntial_variables = self.match_any_with_ticks(SENTNTIAL_VARIABLES)
    self.predicate_variables = self.match_any_with_ticks(PREDICATE_VARIABLES)

  def match_any(self, iterable):
    """
    Returns a regex which matches any character in "iterable."
    """
    return "[%s]" % ''.join(iterable)

  def match_any_with_ticks(self, iterable):
    """
    Returns a regex which matches any character in "iterable" and is followed by
    zero or more TICK marks, where TICK is a global variable.
    """
    return "{0}{1}*".format(self.match_any(iterable), TICK)

  def scan(self, string):
    """
    Scans an input string for tokens, and returns them.
    """
    scanner = Scanner([
      (self.constant_signs, lambda _, tok: (self.constant_type, tok)),
      (self.numerical_variables, lambda _, tok: (self.numerical_type, tok)),
      (self.sentntial_variables, lambda _, tok: (self.sentntial_type, tok)),
      (self.predicate_variables, lambda _, tok: (self.predicate_type, tok))])

    tokens, remainder = scanner.scan(string)
    if remainder:
      if len(remainder) > 10:
        remainder = remainder[:10]
      raise LexicalException("Error lexing input near {0}...".format(remainder))
    return tokens


class State:
  """
  A container for the program's main data structures, as well as high-level
  methods for operating on them.
  """
  def __init__(self):
    self.encoding = []
    self.numerical_variables = {}
    self.sentntial_variables = {}
    self.predicate_variables = {}

  def next_var_name(self, assigned, pool):
    """
    Creates a new variable name.

    assigned: A list of all of the variable names already assigned.
    pool: A list of all valid variable names.
    """
    poollen = len(pool)
    count = len(assigned)
    ticks = count // poollen
    name = pool[count % poollen] + TICK * ticks
    return name

  def encode_constant_sign(self, symbol):
    """
    Encodes a constant sign, as defined by the global variable CONSTANT_SIGNS
    into a number.
    """
    return CONSTANT_SIGNS.mapping.get(symbol)

  def encode_numerical_variable(self, symbol):
    """
    Encodes a numerical variable, as defined by the global variable
    NUMERICAL_VARIABLES into a number.
    """
    gnum = self.numerical_variables.get(symbol)
    if gnum:
      return gnum
    else:
      gnum = PRIME[PRIME_OFFSET + len(self.numerical_variables)]
      self.numerical_variables[symbol] = gnum
      return gnum

  def encode_sentntial_variable(self, symbol):
    """
    Encodes a sentential variable, as defined by the global variable
    SENTNTIAL_VARIABLES into a number.
    """
    gnum = self.sentntial_variables.get(symbol)
    if gnum:
      return gnum
    else:
      gnum = PRIME[PRIME_OFFSET + len(self.sentntial_variables)]**2
      self.sentntial_variables[symbol] = gnum
      return gnum

  def encode_predicate_variable(self, symbol):
    """
    Encodes a predicate variable, as defined by the global variable
    PREDICATE_VARIABLES into a number.
    """
    gnum = self.sentntial_variables.get(symbol)
    if gnum:
      return gnum
    else:
      gnum = PRIME[PRIME_OFFSET + len(self.sentntial_variables)]**3
      self.sentntial_variables[symbol] = gnum
      return gnum

  def decode_numerical_variable(self, gnum):
    """
    Assigns a numerical variable to gnum.
    """
    symbol = self.numerical_variables.get(gnum)
    if symbol:
      return symbol
    symbol = self.next_var_name(self.numerical_variables, NUMERICAL_VARIABLES)
    self.numerical_variables[gnum] = symbol
    return symbol

  def decode_sentential_variable(self, gnum):
    """
    Assigns a sentential variable to gnum.
    """
    symbol = self.sentntial_variables.get(gnum)
    if symbol:
      return symbol
    symbol = self.next_var_name(self.sentntial_variables, SENTNTIAL_VARIABLES)
    self.sentntial_variables[gnum] = symbol
    return symbol

  def decode_predicate_variable(self, gnum):
    """
    Assigns a predicate variable to gnum.
    """
    symbol = self.predicate_variables.get(gnum)
    if symbol:
      return symbol
    symbol = self.next_var_name(self.predicate_variables, PREDICATE_VARIABLES)
    self.predicate_variables[gnum] = symbol
    return symbol

    
def encode(string):
  """
  Encodes a string from the formal system PM as a Gödel number.
  
  The alphabet is as follows:
    ~ ∨ ⊃ ∃ = 0 s () , + × 
  With variables of the form:
    x, y, z , p, r, q, P, R, Q, x`, x``, ...
  """
  if not string: return 0

  state = State()
  lexer = Lexer()
  tokens = lexer.scan(string)

  lexmap = {
    lexer.constant_type  : state.encode_constant_sign,
    lexer.numerical_type : state.encode_numerical_variable,
    lexer.sentntial_type : state.encode_sentntial_variable,
    lexer.predicate_type : state.encode_predicate_variable
  }

  for token_type, lexeme in tokens:
    lookup = lexmap[token_type]
    gnum = lookup(lexeme)
    state.encoding.append(gnum)
  retval = prod(PRIME[idx]**gnum for idx, gnum in enumerate(state.encoding))
  return retval


def decode(number):
  """
  Decodes a Gödel number into a string from the formal system PM.
  """
  if not number: return ""

  state = State()

  symbols = []
  factors = ((k, len(list(v))) for k, v in groupby(factor(number)))
  for i, (f, gnum) in enumerate(factors):
    if PRIME[i] != f:
      err = "not a Gödel number: prime at index {0} is {1} but should be {2}."
      err = err.format(i, f, PRIME[i])
      raise ValueError(err)

    symbol = CONSTANT_SIGNS.inverse.get(gnum)
    if not symbol:
      if gnum in PRIME:
        symbol = state.decode_numerical_variable(gnum)
      else:
        factors = factor(gnum)
        if len(set(factors)) != 1:
          err = '{0} is not prime, a prime squared, or a prime cubed.'
          err = err.format(gnum)
          raise ValueError(err)

        if len(factors) == 2 and factors[0] in PRIME:
          symbol = state.decode_sentential_variable(gnum)
        elif len(factors) == 3 and factors[0] in PRIME:
          symbol = state.decode_predicate_variable(gnum)
        else:
          err = '{0} is not prime, a prime squared, or a prime cubed.'
          err = err.format(gnum)
          raise ValueError(err)

    symbols.append(symbol)
  return ''.join(symbols)  
  
  
if __name__ == '__main__':
  test_string1 = '0=0'
  test_string2 = '(∃pPx)(x=sy)'

  encoded_test_string1 = encode(test_string1)
  encoded_test_string2 = encode(test_string2)

  print(encoded_test_string1)
  print(encoded_test_string2)

  decoded_test_string1 = decode(encoded_test_string1)
  decoded_test_string2 = decode(encoded_test_string2)

  print((test_string1, encoded_test_string1, decoded_test_string1))
  print((test_string2, encoded_test_string2, decoded_test_string2))
