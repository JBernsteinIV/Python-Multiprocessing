#!/usr/bin/python

# Easy way to loop backwards in Python 3
names  = ['raymond', 'rachel', 'matthew']
colors = ['red','green','blue','yellow']

for color in reversed(colors):
	print color

# Enumerate will loop over indices
for i, color in enumerate(colors):
	print i, '-->', colors[i]

# Loop over two collections - SLOW. Zip makes a new tuple.
for name, color in zip(names, colors):
	print name, '-->', color

# izip is more performant. Python 3, not Python 2.7.
#for name, color in izip(names, colors):
#	print name, '-->', color

# Calls a function until a sentinel value
blocks = []
for block in iter(partial(f.read,32), ''):
	blocks.append(block)

# Distinguising multiple exit points in loops
def find(seq, target):
	for i, value in enumerate(seq):
		if value == tgt:
			break
	else:
		return -1
	return i

# Looping over dictionary keys

d = {'matthew': 'blue', 'rachel': 'green', 'raymond':'red'}

for k in d:
	print k

# Construct a dictionary from pairs. Python 3.
# d = dict(izip(names,colors))

# Counting with dictionaries
d = {}
for color in colors:
	if color not in d:
		d[color] = 0
	d[color] += 1
# Using the dictionary module's internal API, we can use the get method to simplify the above.

for color in colors:
	d[color] = d.get(color, 0) + 1

# The more modern way for counting with dictionaries
d = defaultdict(int)
for color in colors:
	d[color] += 1

# Grouping with dictionaries

names = {'Raymond', 'Rachel', 'Matthew', 'Roger',
	'Betty', 'Melissa', 'Judith', 'Charlie'}
d = {}
for name in names:
	key = len(name)
	if key not in d:
		d[key] = {}
	d[key].append(name)
# Better way to group
for name in names:
	key = len(name)
	d.setdefault(key, []).append(name)

#Modern way
d = defaultdict(list)
for name in names:
	key = len(name)
	d[key].append(name)

#Is dictionary popitem() atomic?
d = {'Matthew': 'Blue', 'Rachel':'Green', 'Raymond':'Red'}
while d:
	key, value = d.popitem()
	print key, '-->', value


#Linking dictionaries
defaults = {'color':'red', 'user':'guest'}
parser = argparse.ArgumentParser()
parser.add_argument('-u','--user')
parser.add_argument('-c', '--color')
namespace = parser.parse_args([])
command_line_args = {
	k:v for k, v in
	vars(namespace).items() if v
}
d = defaults.copy()
d.update(os.environ)
d.update(command_line_args)
# In Python 3, ChainMap was included
# d = ChainMap(command_line_args, os.environ, defaults)

# Clarify function calls with keyword arguments
# twitter_search('@obama', retweets=False, numtweets=20, popular=True)

# Clarify multiple return values with named tuples
# doctest.testmod()
# TestResults(failed=0, attempted=4)
#TestResults = namedtuple('TestResults', ['failed', 'attempted'])

# Unpacking sequences
p = 'Raymond', 'Hettinger', 0x30, 'python@example.com'

fname, lname, age, email = p

# Updating multiple state variables
def fibonnacci(n):
	x, y = 0, 1
	for i in range(n):
		print x
		x, y = y, x+y

# Simultaneous state updates
x, y, dx, dy = (x + dx * t,
		y + dy * t,
		influence(m, x, y, dx, dy, partial='x'),
		influence(m, x, y, dx, dy, partial='y'))

# Concatenating strings with O(n) performance
s = names[0]
for name in names[1:]:
	s += ', ' + name
print s

print ', '.join(names)

# Updating sequences
names = deque(['Raymond', 'Rachel', 'Matthew', 'Roger', 'Betty', 'Melissa', 'Judith', 'Charlie'])

# Decorators and context managers
# Helps separate business logic from administrative logic
# Clean, beautiful tools for factoring code and improving code reuse
# Good naming is essential.
# Remember the spiderman rule: With great power comes great responsibility.

# @cache will cache results so that duplicate logic like a repeated URL do not need to perform expensive lookups.
#NOTE: @cache will only work with pure functions. Pure functions are those that return the same answer everytime they are called.
@cache
def web_lookup(url):
	return urllib.urlopen(url).read()

def cache(func):
	saved = {}
	@wraps(func)
	def newfunc(*args):
		if args in saved:
			return newfunc(*args)
		result = func(*args)
		saved[args] = result
		return result
	return newfunc

#Factor out temporary contexts
with localcontext(Context(prec=50)):
	print Decimal(355) / Decimal(113)

#Open and close files
with open('data.txt') as f:
	data = f.read()

# How to use locks
lock = threading.Lock()
with lock:
	print 'Critical section 1'
	print 'Critical section 2'

#Factor out temporary contexts
with ignored(OSError):
	os.remove('somefile.tmp')

# Context manager: ignored()
@contextmanager
def ignored(*exceptions):
	try:
		yield
	except exceptions:
		pass

with open('help.txt', 'w') as f:
	with redirect_stdout(f):
		help(pow)

@contextmanager
def redirect_stdout(fileobj):
	oldstdout = sys.stdout
	sys.stdout = fileobj
	try:
		yield fileobj
	finally:
		sys.stdout = oldstdout


