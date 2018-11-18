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
	for v, group in groups:
		try:
			edges = set()
			for (v, u) in group:
				edges.add(u)
			if not '$' in edges:
				n += 1
				m += len(edges)
				for u in edges:
					print('{}\t{}'.format(u, v))
			else:
				print('{}\t{}'.format(v, '$'))
		except ValueError:
			pass
 	
if __name__ == '__main__':
    main()
