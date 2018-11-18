import sys

# Getting threshold
t = float(sys.argv[1])

# Mapping "Good" Edges only
for line in sys.stdin:
	if line.startswith('#'):
		continue
	
	tokens = line.strip().split('\t')
	if line.startswith('d'):
		degree = int(tokens[2])
		if(degree < t):
			print('{}\t{}'.format(tokens[1], '$'))
	else:
		print('{}\t{}'.format(tokens[1], tokens[0]))
