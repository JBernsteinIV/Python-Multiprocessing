#!/usr/bin/python3

#Concurrency in Python
#Courtesy of Raymond Hettinger, PyBay 2017 Keynote
#Youtube: https://www.youtube.com/watch?time_continue=161&v=9zinZmE3Ogk

#Threading, multiprocessing, and asyncio

#CPYthon has a Global Interpreter Lock (GIL) which limits up to one thread per process. Because of the GIL, leveraging multithreading will make a program's performance drop. However multiprocessing can help leverage the amount of threads running at one time on a machine.

#Threads vs. Processes
#Threads are powerful in terms of utilizing shared state however when shared state is not managed correctly there is a high likelihood of race conditions occurring. This is one reason for the GIL.
#Processes are powerful in their independence from one another but their weakness is a lack of proper communication channels without IPCs like pipes, named pipes (FIFOs), and shared memory / shmem. There is also a performance overhead from managing IPCs. This performance overhead is due to a process of "pickling" information to communicate which then must be "unpickled" on the other side across a medium like a raw socket. Modulation would be an example of pickling, for example.

#Threads vs. Async
#Threads switch preemptively which is convenient so you don't need to explicitly cause a task switch but to prevent data loss, critical sections must be guarded by locks such as semaphores. The limit on the number of threads a machine can run is total CPU power minus the cost of task switching and synchronization.
#Async switches cooperatively so you need to add yield or await statements to properly coordinate task switches. However you now control task switches so locks such as mutexes need to be implemented and synchronization is no longer supported.

#Calling pure Python functions has more overhead than restarting generators or awaitable objects. Awaitable objects use generators under the hood. Every Python function has to build up its state and build a new stack frame on every call whereas generators do not close their stack frame, they simply update state on every call to the generator object.

#Async requires that EVERYTHING be non-blocking however, so things like file I/O cannot be performed for async operations. Opening and closing files creates a file lock to prevent inconsistent state between multiple copies of a file and async removes locks altogether. Special async support tools must be leveraged instead.
"""
THREADING

import random
import threading
import time

FUZZ = True
counter = 0

def worker():
	global counter
	counter += 1
	print(counter)

print('Starting up')
for i in range(10):
	threading.Thread(target=worker).start()
print('Finishing up')
"""
#To help test for race conditions in multithreaded code, fuzzing can be employed. Fuzzing amplifies race condition errors to make them more visible.
"""
def fuzz():
	if FUZZ:
		time.sleep(random.random())
def worker():
	global counter
	fuzz()
	oldctr = counter
	fuzz()
	counter = oldctr + 1
	fuzz()
	print('The count is %d' % counter)
	fuzz()
	print()
	fuzz()
	print()
	fuzz()
	print('-----------')
	fuzz()
	print()

print('Starting up')
fuzz()
for i in range(10):
	threading.Thread(target=worker).start()
	fuzz()
print('Finishing up')	
"""
#	THE FOLLOWING NOTES ARE COURTESY OF MOZILLA AND RAYMOND HETTINGER

#All shared resources are to run in exactly one thread and all communication with that thread must be done through an atomic message queue such as the Queue module or message queues like RabbitMQ. Communication with a database works as well.

#Resources needed: global variables, user input, output devices, files, sockets, etc.

#Some resources that are already have locks inside (thread-safe) are: logging modules, decimal module (thread local variables), databases (reader locks and writer locks), and email (atomic message queue).

#For things that need to happen sequentially, put them into the same thread in sequential order.

#To implement a barrier that waits for parallel threads to complete, use join() to join all of the threads together.

#You cannot wait on daemon threads since they are infinite loops. Use join() on the queue itself. It will wait on all of the requested tasks are marked as being done.

#Sometimes you need a global variable to communicate between functions. Global variables work great for single threaded programs. In multi-threaded programs global mutable state is a disaster. The better solution is to use a threading.local() that is global WITHIN a thread but not outside of a thread.

#Never try to kill a thread from something external to that thread. You never know if a thread is holding a lock. Python doesn't provide a direct mechanism for killing threads externally but using ctypes it's possible. However doing so is a recipe for a deadlock.

#If you need to have the ability to kill a task working on some shared state or anything that uses locks, use multiprocessing instead of multithreading. If you're going to use multithreading, do not kill threads. Allow them to release their locks and exit gracefully after checking a message queue or a global variable.
"""
import queue
import threading

ctr = 0
ctr_queue = queue.Queue()

def ctr_manager():
	'I have EXCLUSIVE rights to update the counter variable'
	global ctr

	while True:
		increment = ctr_queue.get()
		ctr += increment
		print_queue.put(
			['The count is %d' % ctr,
			'---------']
			)
		ctr_queue.task_done()

s = threading.Thread(target=ctr_manager)
s.daemon = True
s.start()
del s

print_queue = queue.Queue()

def print_manager():
	'I have EXCLUSIVE rights to call the "print" keyword'
	while True:
		job = print_queue.get()
		for line in job:
			print(line)
		print_queue.task_done()
t = threading.Thread(target=print_manager)
t.daemon = True
t.start()
del t

def worker():
	'My job is to increment the counter and print the current count'
	ctr_queue.put(1)
print_queue.put(['Starting up'])
worker_threads = []
for i in range(10):
	thread = threading.Thread(target=worker)
	worker_threads.append(thread)
	thread.start()
for thread in worker_threads:
	thread.join()
"""
#Note: A good development strategy is to use map to test code in a single process and single thread mode between switching to multi-processing. Sometimes multithreading will result in code that "hangs", meaning it takes a long time for the threads to finish and display an output.

#What is parallelizeable? Parallelizeable vs. intrinisically serial.
#Amdahl's Law: Often used in parallel computing to predict the theoretical speedup when using multiple processors. For example, if a program needs 20 hours when using a single core and a particular part of the program takes one hour to execute cannot be parallelized while the remaining 19 hours can be parallelized, then regardless of how many processors are devoted to a parellelized execution, the minimum execution time cannot be less than that of the critical one hour. Thus the theoretical speedup is limited to at most 20 times (1 / (1 - p) = 20). For this reason parallel computing is relevant only for a low number of processors and very parallelizable programs.
"""
def sitesize(url):
	'''
	This is non-parallelizeable:
	* UDP DNS request for the url
	* UDP DNS response
	* Acquire socket from the OS
	* TCP Connection: SYN, ACK, SYN/ACK
	* Send HTTP Request for the root resource
	* Wait for the TCP response which is broken into packets.
	* Count the cahracters of the webpage.
	
	This is a bit parallizeable:
	Do ten times in parallel(channel bonding):
		1) DNS lookup(UDP request and response)
		2) Acquire the socket
		3) Send HTTP range requests
		4) The sections come back in parallel across different pieces of fiber.
		5) Count the characters for a single block as received.
	Add up the 10 results.
	'''
	u = urllib.request.urlopen(url)
	page = u.read()
	return url, len(page)
"""
#POOL OF PROCESSES
import urllib.request
from multiprocessing.pool import ThreadPool as Pool

sites = [
	'http://www.yahoo.com/',
	'http://www.cnn.com',
	'http://www.python.org',
	'http://www.jython.org',
	'http://www.pypy.org',
	'http://www.perl.org',
	'http://www.cisco.com',
	'http://www.facebook.com',
	'http://www.twitter.com',
	'http://www.macrumors.com',
	'http://www.arstechnica.com/',
	'http://www.reuters.com/',
	'http://www.abcnews.go.com/',
	'http://www.cnbc.com/'
	]

def sitesize(url):
	with urllib.request.urlopen(url) as u:
		page = u.read()
		return url, len(page)
pool = Pool(10)
#imap_unordered is use to improve responsiveness.
for result in pool.imap_unordered(sitesize, sites):
	print(result)

#Combining Threading and Forking

#The general rule is "thread after you fork not before". Otherwise, the locks used by the thread executor will get duplicated across processes. If one of those processes dies while it has the lock, all of the other processes using that lock will deadlock.


