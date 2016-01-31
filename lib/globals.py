from builtin import Builtin, car, cdr, cons, isatom, isnull, iseq
import operator as op


def add_globals(env):
    """Setups the global names and register the builtin procedures"""
    env.update({
        'cdr': Builtin(cdr, 'cdr'),
        'car': Builtin(car, 'car'),
        'cons': Builtin(cons, 'cons'),
        'atom?': Builtin(isatom, 'atom?'),
        'null?': Builtin(isnull, 'null?'),
        'eq?': Builtin(iseq, 'eq?'),
        'add1': Builtin(lambda x: x + 1, 'add1'),
        'sub1': Builtin(lambda x: x - 1, 'sub1'),
        # 'equal?':   is_equal,
        # 'zero?':    is_zero,
        # 'member?':  is_member,
        # 'number?':  is_number,
        # 'map':      map_,

        '+': Builtin(op.add),
        '-': Builtin(op.sub),
        '*': Builtin(op.mul),
        '/': Builtin(op.div),
        '>': Builtin(op.gt),
        '<': Builtin(op.lt),
        '>=': Builtin(op.ge),
        '<=': Builtin(op.le),
        '=': Builtin(op.eq),
        '^': Builtin(op.pow),
        'not': Builtin(op.not_),

        # var
        '#t': True,
        '#f': False,
        'else': True,
    })
    return env
