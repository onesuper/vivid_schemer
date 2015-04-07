

def add_builtins(env):
    """
    the first call to eval should set up the global functions
    """

    env.update({
        '+':        add,
        '-':        sub,
        '*':        mult,
        '/':        div,
        'add1':     add1,
        'sub1':     sub1,
        '^':        expt,
        'not':      not_,
        '>':        gt,
        '<':        lt,
        '>=':       gte,
        '<=':       lte,
        '=':        eq, 
        'cons':     cons,
        'car':      car,
        'cdr':      cdr,
        'null?':    is_null,
        'atom?':    is_atom,
        'eq?':      is_eq,
        'equal?':   is_equal,
        'zero?':    is_zero,
        'member?':  is_member,
        'number?':  is_number,
        '#f':       False,
        '#t':       True,
        'else':     True,
        'map':      map_,
    })
    return env

