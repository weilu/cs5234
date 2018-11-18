import sys
from itertools import groupby
from operator import itemgetter

def read_from_mapper(file):
	for edges in file:
		yield edges.split()

def main():
	n = m = 0

	data = read_from_mapper(sys.stdin)
	groups = groupby(data, itemgetter(0)) # 0 for u/sourceNode and 1 for v/destNode
	for u, group in groups:
		try:
			n+=1
			degree=0
			for u, v in group:
				print('{}\t{}'.format(u, v))
				degree+=1
			m+=degree
			print('{}\t{}\t{}'.format('d', u, degree))
		except ValueError:
			pass
 
	file = open('cache.temp','a') 
	 
	file.write('n\t'+str(n)+'\n') 
	file.write('m\t'+str(m)+'\n')   
	 
	file.close()

if __name__ == '__main__':
    main()
