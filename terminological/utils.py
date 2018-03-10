from math import gcd
from functools import reduce

# Constants
INF = float('inf')


def matrix_to_string(matrix):
    return '\n'.join([''.join([c.character for c in row]) for row in matrix])


def matrix_slice(matrix, row_start, row_len, col_start, col_len):
    return [r[col_start:col_start + col_len]
            for r in matrix[row_start:row_start + row_len]]


def gcd_of(collection):
    return reduce(gcd, collection)


def split(string, size):
    if size == 0:
        return [string]
    strings = string.replace('\t', '    ').split('\n')
    result = []
    for substring in strings:
        result.extend([substring[i:i+size] for i in range(0, len(substring), size)])
    return result


def fit_to_length(string: str, length: int,
                  left_cap: str = None, right_cap: str = None,
                  filler: str = None):
    """Given a string and a length, this function either pads it with a filler character (' ' by
       default) or truncates it. Can also be given left and right end-cap characters."""
    left_cap = left_cap[0] if left_cap is not None else ''
    right_cap = right_cap[0] if right_cap is not None else ''
    filler = filler if filler is not None else ' '

    result = left_cap + string + (filler * (length - (len(string) + len(left_cap) + \
             len(right_cap)))) + right_cap

    if length <= 6:
        return result[:(length-1 if right_cap else length)] + (result[-1] if right_cap else '')
    else:
        if length < len(result):
            return result[0:(length-5 if right_cap else length-4)] + '...' + \
                   result[(-2 if right_cap else -1):]
        return result


class SizeDef(object):
    def __init__(self, _, weight, min_s, max_s):
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
    definitions = [SizeDef(*t) for t in dimension_list]
    scalar = gcd_of({d.weight for d in definitions})
    [d.scale(scalar) for d in definitions]

    # grow each element according to weight until we cannot grow further
    size = sum(d.size for d in definitions)
    while 42:
        if any(d.delta for d in definitions):
            for size_def in definitions:
                if size < total_size:
                    size += size_def.grow()
                    if size > total_size:
                        size_def.size -= size - total_size
                        return [d.tup for d in definitions]
                else:
                    return [d.tup for d in definitions]
        else:
            return [d.tup for d in definitions]
