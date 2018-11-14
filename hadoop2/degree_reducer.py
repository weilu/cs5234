#!/usr/bin/env python
import sys
from itertools import groupby
from operator import itemgetter
from util import read_mapper_output


for line in sys.stdin:
    data = read_mapper_output(sys.stdin)
    groups = groupby(data, itemgetter(0))
    for u, group in groups:
        degree = 0
        for u, v in group:
            degree += 1
            print('{}\t{}'.format(u, v))
        print('{}\td\t{}'.format(u, degree))
