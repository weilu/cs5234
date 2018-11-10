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
		n+=1
		try:
			degree = sum(1 for u, v in group)
			m+=degree
			print (u, degree)
		except ValueError:
			pass
 
	file = open('cache.temp','w') 
	 
	file.write('n\t'+str(n)+'\n') 
	file.write('m\t'+str(int(m/2))+'\n')   
	 
	file.close()

if __name__ == '__main__':
    main()
