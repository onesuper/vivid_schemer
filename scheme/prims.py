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
        # '*':        mult,
        # '/':        div,
        # 'add1':     add1,
        # 'sub1':     sub1,
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
    retval = a.value + b.value
    e.answer("{0}.".format(retval))
    return retval


def sub(a, b, lv):
    e = Echo("sub", lv)
    e.ask("What's the result of {0} - {1}?".format(to_lisp_str(a), to_lisp_str(b)))
    retval = a.value - b.value
    e.answer("{0}.".format(retval))
    return retval
