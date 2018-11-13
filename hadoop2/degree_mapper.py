#!/usr/bin/env python
import sys


for line in sys.stdin:
    if line.startswith('#'):
        continue
    nodes = line.split()
    print('{}\t{}'.format(nodes[0], 1))
    print('{}\t{}'.format(nodes[1], 1))
