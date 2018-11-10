import sys

# Reading graph info (n, m, epsilon) from cache file
cache = open('cache.temp','r')
n = m = epsilon = 0
for line in cache:
	tokens = line.strip().split('\t')
	try:
		if (tokens[0] == 'n'):
			n = int(tokens[1])
		elif (tokens[0] == 'm'):
			m = int(tokens[1])
		elif (tokens[0] == 'epsilon'):
			epsilon = float(tokens[1])
	except ValueError:
		pass
cache.close()

t = 2*(1+epsilon)*m/n

# Getting degree list
degree = open('degree.temp','r')
A_S = set()

for line in degree: 
	pair = line.strip().split()
	
	if(int(pair[1]) <= t):
		A_S.add(int(pair[0]))
degree.close()
# Mapping "Good" Edges only
for line in sys.stdin:
	edges = line.strip().split('\t')
	if edges[0].startswith('#'):
		continue
	if int(edges[0]) in A_S or int(edges[1]) in A_S:
		continue

	print(int(edges[0]), int(edges[1]))

