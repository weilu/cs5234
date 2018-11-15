import sys
from itertools import groupby
from operator import itemgetter

def read_from_mapper(file):
    for edges in file:
        yield edges.strip().split('\t')

def main():
	n = m = 0

	data = read_from_mapper(sys.stdin)
	groups = groupby(data, itemgetter(0)) # 0 for u/sourceNode and 1 for v/destNode
	for u, group in groups:
		try:
			edges = set()
			for (u, v) in group:
				edges.add(v)
			if not '$' in edges:
				n += 1
				m += len(edges)
				print('{}\t{}\t{}'.format('d', u, len(edges)))
				for v in edges:
					print('{}\t{}'.format(u, v))
		except ValueError:
			pass
	file = open('cache.temp','a') 
	 
	file.write('n\t'+str(n)+'\n') 
	file.write('m\t'+str(m)+'\n')   
	 
	file.close()
 
if __name__ == '__main__':
    main()
