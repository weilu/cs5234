import os, sys

def read_from_cache():
	# Reading graph info (n, m) from cache file
	cache = open('cache.temp','r')
	n = m = 0
	for line in cache:
		tokens = line.strip().split('\t')
		try:
			if (tokens[0] == 'n'):
				n = int(tokens[1])
			elif (tokens[0] == 'm'):
				m = int(tokens[1])
		except ValueError:
			pass

	return (n,m)

def main(argv):
	filepath = argv[1]
	epsilon = argv[2]

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

	os.system('hdfs dfs -rm -r /user/hduser/'+filename+'.temp/ > local.log')
	os.system('hdfs dfs -mkdir /user/hduser/'+filename+'.temp/ > local.log')
	os.system('hdfs dfs -put -f'+' '+filepath+' '\
				+'/user/hduser/'+filename+'.temp/graph.temp > local.log')

	while(True):
		os.system('./hadoop_densest_subgraph.sh'+' '\
				+filename+' '+str(epsilon)+' > local.log')
		(n,m) = read_from_cache()
		print(n, m)
		if (n==0):
			break

		new_density = m/n;
		if(new_density > opt_density):
			opt_n = n
			opt_m = m
			opt_density = new_density
			os.system('hdfs dfs -cp -f /user/hduser/'+filename+'.temp/graph.temp'\
				+' '+'/user/hduser/'+filename+'.temp/graph.clone > local.log')
	
	os.system('hdfs dfs -cp -f /user/hduser/'+filename+'.temp/graph.clone'+' '\
		+'/user/hduser/'+filename+'.out > local.log')

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

