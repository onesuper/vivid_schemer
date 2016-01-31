from errors import VividRuntimeError
from builtin import car, cdr, isnull


def flat_list(x):
    """Flat a S-expression to a list representaion
    e.g (x y z) => [x, y, z]"""
    l = []
    while True:
        if isnull(x):
            break
        l.append(car(x))
        x = cdr(x)
    return l


def unique_id():
    """
    Use to assign unique id for each atom
    """

    count = [0]

    def incr():
        count[0] += 1
        return count[0]
    return incr


def check_parameters(expect, real):
    if real != expect:
        raise VividRuntimeError('requires %d arguments(s)' % expect)


def ordinal(n):
    """
    Returns an ordinal number decorated string (e.g. '2nd')
    @param n  A integer number
    """

    if 4 <= n <= 20 or 24 <= n <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][n % 10 - 1]
    return str(n)+suffix
