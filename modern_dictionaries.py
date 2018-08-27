#!/usr/bin/python3

# Instance Dictionaries
# Create a class to track user assignments within a property category.
"""
from __future__ import division, print_function
import sys

class UserProperty:
	def __init__(self, v0, v1, v2, v3, v4):
		self.guido = v0
		self.sarah = v1
		self.barry = v2
		self.rachel = v3
		self.tim = v4
	def __repr__(self):
		return 'UserProperty(%r\r\n, %r\r\n, %r\r\n, %r\r\n, %r\r\n)' \
			% (self.guido, self.sarah, self.barry, self.rachel, self.tim)

colors = UserProperty('blue','orange','green','yellow','red')
cities = UserProperty('austin','dallas','tucson','reno','portland')
fruits = UserProperty('apple','banana','orange','pear','peach')

for user in [colors, cities, fruits]:
	print(vars(user))
	print("\n")

print(list(map(sys.getsizeof, map(vars, [colors, cities, fruits]))))
"""
# Evolution - In the beginning, there were databases.

from __future__ import division, print_function
from pprint import pprint

keys = 'guido sarah barry rachel tim'.split()
v1 = 'blue orange green yellow red'.split()
v2 = 'austin dallas tuscon reno portland'.split()
v3 = 'apple banana orange pear peach'.split()
hashes = list(map(abs, map(hash, keys)))
entries = list(zip(hashes, keys, v1))
comb_entries = list(zip(hashes, keys, v1, v2, v3))

# How a database would do it
def database_linear_search():
	pprint(list(zip(keys, v1, v2, v3)))

# How LISP would do it
def association_lists():
	pprint([
		list(zip(keys, v1)),
		list(zip(keys, v2)),
		list(zip(keys, v3))
	])
# Separate Chaining
def separate_chaining(n):
	buckets = [[] for i in range(n)]
	for pair in entries:
		h, key, value = pair
		i = h % n
		buckets[i].append(pair)
	pprint(buckets)
# Open Addressing
# Make the table more dense. Reduce memory allocator demands. Cope with collisions via linear probing.

def open_addressing_linear(n):
	table = [None] * n
	for h, key, value in entries:
		i = h % n
		while table[i] is not None:
			i = (i + 1) % n
		table[i] = (key, value)
	pprint(table)

# Open Addressing Multiple Hashing = Reduces catastrophic linear pile-up.

def open_addressing_multihash(n):
	table = [None] * n
	for h, key, value in entries:
		perturb = h
		i = h % n
		while table[i] is not None:
			print('%r collided with %r' % (key, table[i][0]))
			i = (5 * i + perturb + 1) % n
			perturb >>= 5
		table[i] = (key, value)
	pprint(table)

# Compact Dict
def compact_and_ordered(n):
	table = [None] * n
	for pos, entry in enumerate(entries):
		h = perturb = entry[0]
		i = h % n
		while table[i] is not None:
			i = (5 * i + perturb + 1) % n
			perturb >>= 5
		table[i] = pos
	pprint(entries)
	pprint(table)

# Key-Sharing Dict
def shared_and_compact(n):
	'Compact, ordered, and shared'
	table = [None] * n
	for pos, entry in enumerate(comb_entries):
		h = perturb = entry[0]
		i = h % n
		while table[i] is not None:
			i = (5 * i + perturb + 1) % n
			perturb >>= 5
		table[i] = pos
	pprint(comb_entries)
	pprint(table)


database_linear_search()
print('------------------------')
association_lists()
print('------------------------')
separate_chaining(2)
print('------------------------')
open_addressing_linear(8)
print('------------------------')
open_addressing_multihash(8)
print('------------------------')
compact_and_ordered(8)
print('------------------------')
shared_and_compact(16)
