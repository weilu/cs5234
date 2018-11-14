#!/usr/bin/env python
import sys


threshold = float(sys.argv[1])
for line in sys.stdin:
    # may be {u d deg} or {u v}
    node_or_deg = line.split()
    if len(node_or_deg) == 3: # {u d deg}
        deg = int(node_or_deg[-1])
        if deg <= threshold:
            print('{}\t$'.format(node_or_deg[0]))
    else:
        print('{}\t{}'.format(node_or_deg[0], node_or_deg[1]))
