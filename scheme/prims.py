from cmdline import Echo
from utils import to_lisp_str


def add_globals(env):
    """
    the first call to eval should set up the global functions
    """

    env.update({
        'quit':       quit,
        '+':        add,
        '-':        sub,
        '*':        mult,
        '/':        div,
        'add1':     add1,
        'sub1':     sub1,
        # '^':        expt,
        # 'not':      not_,
        # '>':        gt,
        # '<':        lt,
        # '>=':       gte,
        # '<=':       lte,
        # '=':        eq,
        # 'cons':     cons,
        # 'car':      car,
        # 'cdr':      cdr,
        # 'null?':    is_null,
        # 'atom?':    is_atom,
        # 'eq?':      is_eq,
        # 'equal?':   is_equal,
        # 'zero?':    is_zero,
        # 'member?':  is_member,
        # 'number?':  is_number,
        # '#f':       False,
        # '#t':       True,
        # 'else':     True,
        # 'map':      map_,
    })
    return env

def quit(lv):
    import sys
    sys.exit()


def add(a, b, lv):
    e = Echo("add", lv)
    e.ask("What's the result of {0} + {1}?".format(to_lisp_str(a), to_lisp_str(b)))
    e.answer("{0}.".format(a+b))
    return a+b


def sub(a, b, lv):
    e = Echo("sub", lv)
    e.ask("What's the result of {0} - {1}?".format(to_lisp_str(a), to_lisp_str(b)))
    e.answer("{0}.".format(a-b))
    return a-b


def mult(a, b, lv):
    e = Echo("mult", lv)
    e.ask("What's the result of {0} * {1}?".format(to_lisp_str(a), to_lisp_str(b)))
    e.answer("{0}.".format(a*b))
    return a*b


def div(a, b, lv):
    e = Echo("div", lv)
    e.ask("What's the result of {0} / {1}?".format(to_lisp_str(a), to_lisp_str(b)))
    if b == 0:
        raise ZeroDivisionError
    e.answer("{0}.".format(a/b))
    return a/b


def add1(a, lv):
    e = Echo("add1", lv)
    e.ask("What is the result of adding 1 to {0}?".format(to_lisp_str(a)))
    e.answer("{0}.".format(a+1))
    return a+1


def sub1(a, lv):
    e = Echo("sub1", lv)
    e.ask("What is the result of subtracting 1 from {0}?".format(to_lisp_str(a)))
    e.answer("{0}.".format(a-1))
    return a-1

