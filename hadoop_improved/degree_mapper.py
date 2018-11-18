import sys

for line in sys.stdin:
	if line.startswith('#'):
		continue
	print(line.strip())
