#!/usr/bin/env python
import sys
from itertools import groupby
from operator import itemgetter
from util import read_mapper_output


for line in sys.stdin:
    data = read_mapper_output(sys.stdin)
    groups = groupby(data, itemgetter(0))
    for u, group in groups:
        remove = False
        for u, v, flag in group:
            if flag == '$':
                remove = True
                continue
            elif remove:
                remove = False
                continue
            else:
                print('{}\t{}'.format(u, v))

