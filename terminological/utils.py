from math import gcd
from functools import reduce

# Constants
INF = float('inf')


def matrix_to_string(matrix):
    return '\n'.join([''.join([c.character for c in row]) for row in matrix])


def matrix_slice(matrix, row_start, row_len, col_start, col_len):
    return [r[col_start:col_start + col_len]
            for r in matrix[row_start:row_start + row_len]]


def gcd_of(s):
    return reduce(gcd, s)


def split(string, size):
    if size == 0:
        return [string]
    strings = string.replace('\t', '    ').split('\n')
    result = []
    for string in strings:
        result.extend([string[i:i+size] for i in range(0, len(string), size)])
    return result


class SizeDef(object):
    def __init__(self, size, weight, min_s, max_s):
        self.size = min_s
        self.weight = weight
        self.scaled_weight = weight
        self.min_s = min_s
        self.max_s = max_s

    def grow(self):
        delta = self.delta
        self.size += delta
        return delta

    @property
    def delta(self):
        return min(self.scaled_weight, self.max_s - self.size)
    
    @property
    def tup(self):
        return (self.size, self.weight, self.min_s, self.max_s)
    
    def scale(self, scalar):
        self.scaled_weight = round(self.weight / scalar, 0)


def compute_sizes(dimension_list, total_size):
    D = [SizeDef(*t) for t in dimension_list]
    scalar = gcd_of({d.weight for d in D})
    [d.scale(scalar) for d in D]

    # grow each element according to weight until we cannot grow further
    size = sum(d.size for d in D)
    while 42:
        if any(d.delta for d in D):
            for d in D:
                if size < total_size:
                    size += d.grow()
                    if size > total_size:
                        d.size -= size - total_size
                        return [d.tup for d in D]
                else:
                    return [d.tup for d in D]
        else:
            return [d.tup for d in D]

