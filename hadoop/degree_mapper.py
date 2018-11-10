import sys

for line in sys.stdin:
	edges = line.strip().split('\t')
	if edges[0].startswith('#'):
		continue
	print(edges[0], 1)
	print(edges[1], 1)
