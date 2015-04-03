#=============================================================
# An interupter for The Little Schemer in Python
# Based on Peter Norvig's lispy.py
# By onesuper
#
# The syntaxes and sementics strictly follow The Little Schemer
#==============================================================



# Use to assign unique id for each atom
def unique_id():
    count = [0]
    def incr():
        count[0] += 1
        return count[0]
    return incr


def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):              # list
        return '('+' '.join(map(to_string, exp))+')'
    elif hasattr(exp, '__call__'):  # function
        return exp.__name__
    elif isinstance(exp, bool):            # bool
        return '#t' if exp else '#f'
    elif exp is None:
        return 'NIL'
    else:                           # number
        return str(exp)


def ordinal(n):
    # ordinal number decoration
    if 4 <= n <= 20 or 24 <= n <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][n % 10 - 1]
    return str(n)+suffix
