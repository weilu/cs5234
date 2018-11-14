#!/usr/bin/env python
import sys
from itertools import groupby
from operator import itemgetter

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator)

for line in sys.stdin:
    data = read_mapper_output(sys.stdin)
    groups = groupby(data, itemgetter(0))
    for u, group in groups:
        remove = False
        for u, v in group:
            if v == '$':
                remove = True
                continue
            if remove:
                # flag in-edges for removal
                print('{}\t{}\t$'.format(v, u))
            else:
                print('{}\t{}\t1'.format(u, v))
