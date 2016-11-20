from vivid_schemer.errors import VividSyntaxError
from vivid_schemer.builtin import *
from vivid_schemer.parser import new_symbol
from vivid_schemer.sexp import SExp, SAtom
import logging


LOG = logging.getLogger(__name__)

_global_envs = {
    'cdr': Builtin(cdr),
    'car': Builtin(car),
    'cons': Builtin(cons),
    'atom?': Builtin(isatom, 'atom?'),
    'list?': Builtin(islist, 'list?'),
    'null?': Builtin(isnull, 'null?'),
    'eq?': Builtin(iseq, 'eq?'),
    'add1': Builtin(lambda x: x + 1, 'add1'),
    'sub1': Builtin(lambda x: x - 1, 'sub1'),
    # 'equal?':   is_equal,
    # 'zero?':    is_zero,
    # 'member?':  is_member,
    # 'number?':  is_number,
    # 'map':      map_,

    # arithmetic
    '+': Builtin(lambda x, y: x + y, 'add'),
    '-': Builtin(lambda x, y: x - y, 'sub'),
    '*': Builtin(lambda x, y: x * y, 'mult'),
    '/': Builtin(lambda x, y: x / y, 'div'),
    '>': Builtin(lambda x, y: x > y, 'gt'),
    '<': Builtin(lambda x, y: x < y, 'lt'),
    '>=': Builtin(lambda x, y: x >= y, 'gte'),
    '<=': Builtin(lambda x, y: x <= y, 'lte'),
    '=': Builtin(lambda x, y: x == y, 'eq'),
    '^': Builtin(lambda x, y: x ** y, 'power'),
    'not': Builtin(lambda x: ~x, 'not'),

    # var
    '#t': True,
    '#f': False,
    'else': True,
}


class Env(dict):
    def __init__(self, parms=(), args=()):
        super(Env, self).__init__()
        self.update(zip(parms, args))


def globals(env=Env()):
    env.update(_global_envs)
    return env


class Procedure(object):
    """User-defined scheme procedure"""

    def __init__(self, params, body, env):
        self._params = params
        self._body = body
        self._env = env

    def __repr__(self):
        return '<Procedure %s, %s>' % (self._params, self._body)

    def __call__(self, args):
        params = to_list(self._params)
        args = to_list(args)
        if len(params) != len(args):
            raise VividRuntimeError('Procedure requires %d argument(s)' % len(params))
        return evaluate(self._body, Env(params, args))


_begin = new_symbol('begin')
_quote = new_symbol('quote')
_define = new_symbol('define')
_cond = new_symbol('cond')
_lambda = new_symbol('lambda')


def evaluate(sexp, env=Env()):
    envs = [env]
    stack = [sexp]

    while len(stack) != 0:
        tos = stack[-1]
        env = envs[-1]
        # tos.set_msg("What's the value of '%s'?" % tos)
        # yield tos, stack, envs

        assert isinstance(tos, SExp)
        if isinstance(tos, SAtom):
            if is_digit_str(tos):
                tos.assign_value(int(str(tos)))
                tos.set_msg('===> integer value: %s' % tos.value, color='green')
            elif is_letter_begin_str(tos):
                var = str(tos)
                tos.assign_value(find_var(var, envs + [env]))
                tos.set_msg('===> variable reference: %s' % tos.value, color='green')
            else:
                raise VividSyntaxError('Unrecognized string: ' + str(tos))
            tos.mark_visited()
            stack.pop()
            envs.pop()
            LOG.debug('pop [%s] ' % tos.id)
        elif car(tos) is _quote:
            require(tos, len(to_list(tos)) == 2)
            quoting = car(cdr(tos))
            tos.assign_value(quoting)
            tos.set_msg('===> quoting: %s' % tos.value, color='green')
            tos.mark_visited()
            stack.pop()
            envs.pop()
            LOG.debug('pop [%s] ' % tos.id)
        elif car(tos) is _define:
            l = to_list(tos)
            require(tos, len(l) == 3)
            _, var, expr = l
            if not expr.is_visited:
                LOG.debug('push [%d]' % expr.id)
                stack.append(expr)
                envs.append(env)
            else:
                tos.set_msg("Define a variable '%s' that equals %s" % (var, expr.value))
                LOG.debug('set env[\'%s\'] = %s' % (var, expr.value))
                envs[-1][str(var)] = expr.value
                tos.mark_visited()
                yield tos, stack, envs
                stack.pop()
                envs.pop()
                LOG.debug('pop [%s] ' % tos.id)
        elif car(tos) is _lambda:
            params = car(cdr(tos))
            body = car(cdr(cdr(tos)))
            tos.set_msg("Lambda creates a procedure with params %s, and %s as body" % (params, body))
            tos.assign_value(Procedure(params, body, env))
            tos.mark_visited()
            stack.pop()
            envs.pop()
            LOG.debug('pop [%s] ' % tos.id)
            yield tos, stack, envs
        elif car(tos) is _begin:
            # (begin () ())
            tos.mark_visited()
            stack.pop()
            envs.pop()
            LOG.debug('pop [%s] ' % tos.id)
            clauses = cdr(tos)
            for clause in reversed(to_list(clauses)):
                LOG.debug('push [%d]' % clause.id)
                stack.append(clause)
                envs.append(env)

        elif car(tos) is _cond:
            # (cond (test conseq) (test conseq)...)
            clauses = cdr(tos)
            n = 0
            while True:
                if isnull(clauses):
                    raise VividRuntimeError("Cond must take at least one true condition")
                clause = car(clauses)
                n += 1
                if not clause.is_visited:
                    test, conseq = car(clause), car(cdr(clause))
                    if not test.is_visited:
                        clause.set_msg("%s question: Is %s true?" % (ordinal(n), test))
                        yield clause, stack, envs
                        test.mark_visited()
                        stack.append(test)
                        envs.append(Env())
                        break
                    if test.value:
                        if not conseq.is_visited:
                            clause.set_msg("Yes. You will get the value of %s" % conseq)
                            conseq.mark_visited()
                            yield clause, stack, envs
                            stack.append(conseq)
                            envs.append(Env())
                            break
                        tos.set_msg("You get %s" % conseq.value)
                        tos.assign_value(conseq.value)
                        yield tos, stack, envs
                        stack.pop()
                        envs.pop()
                        break
                    else:
                        clause.mark_visited()
                        clause.set_msg("Nope. So check the next question")
                        yield clause, stack, envs
                clauses = cdr(clauses)
        else:
            proc = car(tos)
            args = cdr(tos)

            if not proc.is_visited:
                proc.mark_visited()
                stack.append(proc)
                envs.append(Env())
                continue
            proc = proc.value

            if not args.is_visited:
                args.mark_visited()
                y = args
                while True:
                    if isnull(y):
                        break
                    arg = car(y)
                    if not arg.is_visited:
                        arg.mark_visited()
                        stack.append(arg)
                        envs.append(Env())
                    y = cdr(y)
                continue

            args_list = [arg.value for arg in to_list(args)]
            if len(args_list) == 1:
                tos.set_msg('Is it true that this is %s: %s' % (proc.name, args_list[0]), color='red')
            else:
                tos.set_msg("Call %s with %s." % (proc, ', '.join([str(i) for i in args_list])))
            yield tos, stack, envs

            if isinstance(proc, Procedure):
                params_list = [str(parm) for parm in to_list(proc._params)]
                require(args, len(params_list) == len(args_list))

                e = Env(params_list, args_list)
                if not proc._body.is_visited:
                    proc._body.set_msg("What's the value of '%s'?" % proc._body)
                    yield proc._body, stack, envs
                    proc._body.mark_visited()
                    stack.append(proc._body)
                    envs.append(e)
                    continue
                tos.assign_value(proc._body.value)
                tos.set_msg('===> %s' % tos.value, color='green')
                yield tos, stack, envs
                stack.pop()
                envs.pop()
            elif isinstance(proc, Builtin):
                tos.assign_value(proc(*args_list))
                tos.set_msg('===> %s' % tos.value, color='green')
                tos.mark_visited()
                yield tos, stack, envs
                stack.pop()
                envs.pop()
            else:
                raise VividRuntimeError("%s expected to be procedure" % proc)


def require(x, predicate, msg="wrong parameters length"):
    """Signal a syntax error if predicate is false."""
    if not predicate:
        raise VividSyntaxError(str(x) + ': ' + msg)


def find_var(var, envs):
    for i in reversed(range(len(envs))):
        if var in envs[i]:
            return envs[i][var]
    raise VividRuntimeError('unbound variable: %s' % var)


def to_list(x):
    """Flat a S-expression to a list representation
    e.g (x y z) => [x, y, z]"""
    l = []
    while True:
        if isnull(x):
            break
        l.append(car(x))
        x = cdr(x)
    return l


def ordinal(n):
    """
    Returns an ordinal number decorated string (e.g. '2nd')
    @param n  A integer number
    """
    if 4 <= n <= 20 or 24 <= n <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][n % 10 - 1]
    return str(n) + suffix
