import os, sys, time

def readFromCache():
	# Reading graph info (n, m) from cache file
	with open('cache.temp','r') as cache_temp:
		n = m = 0
		for line in cache_temp:
			tokens = line.strip().split('\t')
			try:
				if (tokens[0] == 'n'):
					n += int(tokens[1])
				elif (tokens[0] == 'm'):
					m += int(tokens[1])
			except ValueError:
				pass

	return (n,m)

def main(argv):
	filepath = argv[1]
	epsilon = float(argv[2])

	timestamp = time.strftime("_%Y%b%d_%H%M%S")

	# extract filename from file path
	# extension should not matter (i.e. .txt)
	filename = filepath.split('/')[-1]
	filename = filename.split('.')[0]
	
	print('Running Hadoop Densest Subgraph on:', filename)
	print('Input Graph Path on LocalFS:')
	print(filepath)
	print('Epsilon:', epsilon)

	n = m = 0
	opt_n = opt_m = 0
	opt_density = 0

	os.system('hdfs dfs -mkdir /user/hduser/'+filename+timestamp+' > local.log')
	os.system('hdfs dfs -mkdir /user/hduser/'+filename+timestamp+'/temp/ > local.log')
	os.system('hdfs dfs -put -f'+' '+filepath+' '+'/user/hduser/'+filename+timestamp+'/graph.in > local.log')
	os.system('./degree_hadoop.sh'+' '+filename+timestamp+'>local.log')

	while(True):
		(n,m) = readFromCache()
		t = (1+epsilon)*m/n
		print(n, m, t)
		
		os.system('./remove_edge_hadoop.sh'+' '+filename+timestamp+' '+str(t)+'>local.log')
		
		(n,m) = readFromCache()
		print(n, m)

		if (n==0):
			break

		new_density = m/n;
		if(new_density > opt_density):
			opt_n = n
			opt_m = m
			opt_density = new_density
			os.system('hdfs dfs -cp -f /user/hduser/'+filename+timestamp+'/temp/graph.temp/'\
				+' '+'/user/hduser/'+filename+timestamp+'/temp/graph.clone/ > local.log')
	
	os.system('hdfs dfs -cp -f /user/hduser/'+filename+timestamp+'.temp/graph.clone/'+' '\
		+'/user/hduser/'+filename+timestamp+'.out/ > local.log')

	print()
	print('Results:')
	print('Output Graph Path on HFDS:')
	print(filepath)
	print('# Nodes:', opt_n)
	print('# Edges:', opt_m)
	print('Density:', opt_density)
	print('Normalized Density:', opt_density/2)

if __name__ == '__main__':
    main(sys.argv)

