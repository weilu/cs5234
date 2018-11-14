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
        degree = 0
        for u, v in group:
            degree += 1
            print('{}\t{}'.format(u, v))
        print('{}\td\t{}'.format(u, degree))
