Encodes and decodes "Gödel Numbers" as described in the book "Gödel's Proof" by
Ernest Nagel and James R. Newman.

Example
=======
import godel


gnum = godel.encode("(∃x)(x=sy)")

self.assertEqual(gnum, 172225505803959398742621651659678877886965404082311908389214945877004912002249920215937500000000)

string = godel.decode(172225505803959398742621651659678877886965404082311908389214945877004912002249920215937500000000)

self.assertEqual(string, "(∃x)(x=sy)")
