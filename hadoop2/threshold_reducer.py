#!/usr/bin/env python
import os
import sys
from itertools import groupby
from operator import itemgetter
from util import read_mapper_output


# needs to run in a single reducer
epsilon = int(sys.argv[1])
m, m2, n, threshold, density = 0, 0, 0, 0, 0
for line in sys.stdin:
    data = read_mapper_output(sys.stdin)
    groups = groupby(data, itemgetter(0))
    for label, group in groups:
        if label == 'n':
            n = sum(1 for label, v in group)
        elif label == '2m':
            m2 = sum(int(v) for label, v in group)
            m =  m2 / 2

# only works on a single reducer: m, n values are both available
if n != 0:
    threshold = m2 * (1 + epsilon) / n
    density = m / n
print('{}\t{}\t{}\t{}'.format(m, n, threshold, density))
