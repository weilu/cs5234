#!/usr/bin/env python
import sys


for line in sys.stdin:
    node_deg = line.split()
    print('n\t{}'.format(1))
    print('2m\t{}'.format(node_deg[1]))
