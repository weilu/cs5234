#!/usr/bin/env python
import sys


for line in sys.stdin:
    # may be {u d deg} or {u v}
    node_or_deg = line.split()
    if len(node_or_deg) == 3:
        print('n\t{}'.format(1))
        print('2m\t{}'.format(node_or_deg[-1]))
