#=============================================================
# An interupter for The Little Schemer in Python
# Based on Peter Norvig's lispy.py
# By onesuper
#
# The syntaxes and sementics strictly follow The Little Schemer
#==============================================================

isa = isinstance


def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isa(exp, list):              # list
        return '('+' '.join(map(to_string, exp))+')'
    elif hasattr(exp, '__call__'):  # function
        return exp.__name__
    elif isa(exp, bool):            # bool
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
