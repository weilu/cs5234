#!/usr/bin/env python
import sys


for line in sys.stdin:
    if line.startswith('#'):
        continue
    nodes = line.split()
    print('{}\t{}'.format(nodes[0], nodes[1]))
    print('{}\t{}'.format(nodes[1], nodes[0]))
