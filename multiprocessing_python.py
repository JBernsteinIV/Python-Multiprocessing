#!/usr/bin/python3
# Credit to Pinku Surana for examples
# Youtube: https://www.youtube.com/watch?v=s1SkCYMnfbY

# Multiprocessing with Python
""" Python's Global Interpreter Lock (GIL) makes it impossible to allow
    multiple native threads to execute Python code in parallel.
    The exception to this is that C extensions can release the GIL.
    (e.g. NumPy, I/O, etc).
    Threading library in Python is cooperative concurrency on a single
    native thread.
"""
##################################################
# Computing Pi example using Montecarlo Sequence #
##################################################
"""
from random import random
from math import sqrt, pi

def compute_pi(n):
	i, inside = 0, 0
	while i < n:
		x = random()
		y = random()
		if sqrt(x * x + y * y) <= 1:
			inside += 1
		i += 1
	ratio = 4.0 * inside / n
	return ratio

if __name__ == "__main__":
	mypi = compute_pi(10000000)
	print("My pi: {0}, Error: {1}".format(mypi, mypi - pi))
"""
# multiprocessing library in Python
# Docs page: https://docs.python.org/3.4/library/multiprocessing.html?highlight=process
# multiprocessing library creates new Python processes. There is no shared memory and each process runs 1 thread.
# Data is passed between processes by "pickle" serialization.
# There is support for managed shared data.
# There is some difference between pickling on Linux vs. Windows.

# Easiest way to begin multiprocessing is to use the Pool class.
# The Pool class will create however many processes you request it to create and it will manage data distribution across the processes.
# Primary way to work with the Pool class is using a map function.
# Secondary way is
""" 
from time import sleep
from multiprocessing import Pool

def start_function_for_processes(n):
	sleep(.5)
	result_sent_back_to_parent = n * n
	return result_sent_back_to_parent

if __name__ == '__main__':
	with Pool(processes=5) as p:
		results = p.map(start_function_for_processes, range(200), chunksize=10)
	print(results)

"""
# With pool of service workers
"""
from random import random
from math import sqrt, pi
from multiprocessing import Pool

def compute_pi(n):
	i, inside = 0, 0
	while i < n:
		x = random()
		y = random()
		if sqrt(x * x + y * y) <= 1:
			inside += 1
		i += 1
	ratio = 4.0 * inside / n
	return ratio

if __name__ == "__main__":
	#mypi = compute_pi(40000000)
	with Pool(4) as p:
		pis = p.map(compute_pi, [10000000] * 4)
		print(pis)
		mypi = sum(pis)/4
	print("My pi: {0}, Error: {1}".format(mypi, mypi - pi))
"""
# Process class
# Explicitly creates and manages processes.
# p = Process(target=main_func, args=(arg1,arg2))
# Manually start it with p.start()
# 

#Process Example
"""
from os import getpid
from multiprocessing import Process
def prove_existence():
	print(getpid())

if __name__ == '__main__':
	p = Process(target=prove_existence, args=())
	p.start()
	p.join()
	p2 = Process(target=prove_existence, args=())
	p2.start()
	p2.join()

"""
# Process Communication
# Two ways for IPCs through multiprocessing's Process class
# 1. Queue class
#	Use .push(), .pop() for handling messages.
#	Queue class is one-way communication.
# 2. Pipe class
#	Use .send(), .recv() for handling messages.
#	Pipe is two-way communication.
# Must pass object to child process. 

# Pipe example
"""
import os
from multiprocessing import Process, Pipe
from time import sleep

def ponger(p,s):
	count = 0
	while count < 100:
		msg = p.recv()
		print("Process {0} got message: {1}".format(os.getpid(), msg))
		sleep(1)
		p.send(s)
		count += 1
if __name__ == '__main__':
	parent, child = Pipe()
	proc = Process(target=ponger, args=(child, "ping"))
	proc.start()
	parent.send("pong")
	ponger(parent, "pong")
	proc.join()
"""
# Queue example
"""
import math
import random
from multiprocessing import Process, Queue
from os import getpid

def is_prime(n):
	if n % 2 == 0:
		return False
	for i in range(3, int(math.sqrt(n)+1), 2):
		if n % i == 0:
			return False
	return True

def process_main(q):
	while True:
		n = q.get()
		if n == 0:
			return True
		if is_prime(n):
			print(n)
if __name__ == '__main__':
	q = Queue()
	p = Process(target=process_main, args=(q,))
	p.start()
	for i in range(100):
		q.put(random.randint(0,1000000000))
	q.put(0)
	p.join()
"""
# For pipes, two processes cannot read and write to the same end of a pipe at the same time as this is not built to be process-safe.

# 'Shared' Memory
# Value class and Array class
# Value wraps a single basic type
# Array wraps an array of basic types
# Both use typecodes to indicate types
#	'i' : integer, 'd': double
# Not thread-safe!

# Shared memory example
# Value example
"""
from time import sleep
from multiprocessing import Process, Value, Lock

def counter(c, l):
	for i in range(10):
		sleep(.5)
		l.acquire()
		c.value += 1
		l.release()
	return 0

if __name__ == '__main__':
	v = Value('i', 0)
	l = Lock()
	p1 = Process(target=counter, args=(v,l))
	p2 = Process(target=counter, args=(v,l))
	p1.start()
	p2.start()
	p1.join()
	p2.join()
	print(v.value)
"""
# Avoid locks unless absolutely necessary.
# Synchronization - standard tools available and multiprocessing uses the same API as threading.

# Manager class
# Separate Python process that creates proxies around data structures.
# Shared list and dict.
# Offers Value and Array
# Implements all synchronization classes
# Can be connected to remotely
"""
from time import sleep
from os import getpid
from multiprocessing import Process, Manager

def counter(d):
	d[getpid()] = 0
	for i in range(10):
		sleep(1)
		d[getpid()] += 1
	return 0

if __name__ == '__main__':
	with Manager() as m:
		d = m.dict()
		p1 = Process(target=counter, args=(d,))
		p2 = Process(target=counter, args=(d,))
		p1.start()
		p2.start()
		p1.join()
		p2.join()
		print(d)
"""

# For utilizing multiple processes to communicate configuration information with each other, use Zookeeper instead.

# Only use multiprocessing when your program is CPU-bound. Most programs are not CPU-bound, they are usually I/O bound. 
