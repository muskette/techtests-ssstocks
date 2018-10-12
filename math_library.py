from functools import reduce


def mean(iterable):
    return sum(iterable) / len(iterable)


def n_root(n, x):
    return x ** (1 / float(n))


def prod(iterable):
    return reduce(lambda x, y: x * y, iterable)


def geo_mean(iterable):
    product = prod(iterable)
    size = len(iterable)
    return n_root(size, product)