#!/usr/bin/python3

from multiprocessing import Pool
import time
def squared(n):	
	return n * n

if __name__ == '__main__':
	array = [1,2,3,4,5]
	t = time.time()
	p = Pool(processes=3)
	result = p.map(squared, array)
	p.close()
	p.join()
	print("Pool took: ", time.time()-t)
	t2 = time.time()
	result = []
	for x in range(10000):
		result.append(squared(x))
	print("Serial processing took: ", time.time() - t2)


