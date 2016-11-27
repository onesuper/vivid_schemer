from vivid_schemer.errors import VividSyntaxError
from vivid_schemer.builtin import *
from vivid_schemer.parser import new_symbol
from vivid_schemer.sexp import SExp, SAtom
import logging

LOG = logging.getLogger(__name__)


class Env(dict):
    def __init__(self, **kwargs):
        super(Env, self).__init__()
        self.update(kwargs)

    def __repr__(self):
        return str(self.keys())


class Procedure(object):
    """User-defined scheme procedure"""

    def __init__(self, params, body, env):
        self._params = params
        self._body = body
        self._env = env

    def __repr__(self):
        return '<Procedure %s, %s>' % (self._params, self._body)

    def __call__(self, args):
        params = self._params.to_list()
        args = args.to_list()
        if len(params) != len(args):
            raise VividRuntimeError('Procedure requires %d argument(s)' % len(params))
        e = Env()
        e.update(zip(params, args))
        return evaluate(self._body, e)


_begin = new_symbol('begin')
_quote = new_symbol('quote')
_define = new_symbol('define')
_cond = new_symbol('cond')
_lambda = new_symbol('lambda')


def _repr(v):
    if v is None:
        return 'No Answer'
    elif isinstance(v, bool):
        return '(boolean): %s' % ('Yes' if v else 'No')
    elif isinstance(v, int):
        return '(integer): %r' % v
    elif isinstance(v, SAtom):
        return '(atom): %s' % v
    elif isinstance(v, SExp):
        return '(list): %s' % v
    else:
        return repr(v)


def evaluate(stack, environments):
    while len(stack) != 0:
        tos = stack[-1]
        env = environments[-1]
        LOG.debug('tos: %s' % tos)
        LOG.debug('env: %r' % env)

        assert isinstance(tos, SExp)
        if isinstance(tos, SAtom):
            if tos.isdigits():
                tos.assign_value(int(str(tos)))
                tos.set_msg('===> integer value: %s' % _repr(tos.value), color='green')
            elif tos.startswith_nondigit():
                var = str(tos)
                tos.assign_value(_find_var_in_env(var, environments))
                tos.set_msg('===> variable reference: %s' % _repr(tos.value), color='green')
            else:
                raise VividSyntaxError('Unrecognized string: ' + str(tos))
            tos.mark_visited()
            stack.pop()
            environments.pop()
            LOG.debug('pop %s' % tos)

        elif tos.car is _quote:
            _require(tos, len(tos.to_list()) == 2)
            quoting = tos.cdr.car
            tos.assign_value(quoting)
            tos.set_msg('===> %s' % _repr(tos.value), color='green')
            tos.mark_visited()
            stack.pop()
            environments.pop()
            LOG.debug('pop %s' % tos)

        elif tos.car is _define:
            _require(tos, len(tos.to_list()) == 3)
            _, var, expr = tos.to_list()
            if not expr.is_visited:
                LOG.debug('push %s' % expr)
                stack.append(expr)
                environments.append(env)
            else:
                tos.set_msg("Define a variable '%s' that equals %s" % (var, expr.value))
                LOG.debug('set env[\'%s\'] = %s' % (var, expr.value))
                environments[-1][str(var)] = expr.value
                tos.mark_visited()
                yield tos, stack, environments
                stack.pop()
                environments.pop()
                LOG.debug('pop %s' % tos)

        elif tos.car is _lambda:
            params = tos.cdr.car
            body = tos.cdr.cdr.car
            tos.set_msg("Lambda creates a procedure with params %s, and %s as body" % (params, body))
            tos.assign_value(Procedure(params, body, env))
            tos.mark_visited()
            stack.pop()
            environments.pop()
            LOG.debug('pop %s' % tos)
            yield tos, stack, environments

        # (begin (clauses...))
        elif tos.car is _begin:
            clauses = tos.cdr
            if not clauses.is_visited:
                clauses.mark_visited()
                for clause in reversed(clauses.to_list()):
                    LOG.debug('push %s' % clause)
                    stack.append(clause)
                    environments.append(Env())
                continue

            tos.mark_visited()
            stack.pop()
            environments.pop()
            LOG.debug('pop %s' % tos)

        # (cond (test conseq) (test conseq)...)
        elif tos.car is _cond:
            clauses = tos.cdr
            n = 0
            while True:
                if clauses.isnil():
                    raise VividRuntimeError("Cond must take at least one true condition")
                clause = clauses.car
                n += 1
                if not clause.is_visited:
                    test, conseq = clause.car, clause.cdr.car
                    if not test.is_visited:
                        clause.set_msg("%s question: Is %s true?" % (ordinal(n), test))
                        yield clause, stack, environments
                        test.mark_visited()
                        stack.append(test)
                        environments.append(Env())
                        break
                    if test.value:
                        if not conseq.is_visited:
                            clause.set_msg("Yes. You will get the value of %s" % conseq)
                            conseq.mark_visited()
                            yield clause, stack, environments
                            stack.append(conseq)
                            environments.append(Env())
                            break
                        tos.set_msg("You get %s" % conseq.value)
                        tos.assign_value(conseq.value)
                        yield tos, stack, environments
                        stack.pop()
                        environments.pop()
                        break
                    else:
                        clause.mark_visited()
                        clause.set_msg("Nope. So check the next question")
                        yield clause, stack, environments
                clauses = clauses.cdr

        # (proc (args))
        else:
            proc = tos.car
            args = tos.cdr

            if not proc.is_visited:
                stack.append(proc)
                environments.append(Env())
                LOG.debug('push %s' % proc)
                continue
            proc = proc.value

            if not args.is_visited:
                tos.set_msg("What is '%s'?" % tos, color='red')
                yield tos, stack, environments

                for arg in reversed(args.to_list()):
                    LOG.debug('push %s' % arg)
                    stack.append(arg)
                    environments.append(Env())
                args.mark_visited()
                continue

            # collect arg values
            arg_value_list = [arg.value for arg in args.to_list()]

            if isinstance(proc, Procedure):
                param_list = [str(parm) for parm in proc._params.to_list()]
                _require(args, len(param_list) == len(arg_value_list))
                e = Env()
                e.update(zip((param_list, arg_value_list)))
                if not proc._body.is_visited:
                    proc._body.set_msg("What's the value of '%s'?" % proc._body)
                    yield proc._body, stack, environments
                    proc._body.mark_visited()
                    stack.append(proc._body)
                    environments.append(e)
                    continue
                tos.assign_value(proc._body.value)
                tos.set_msg('===> %s' % _repr(tos.value), color='green')
                yield tos, stack, environments
                stack.pop()
                environments.pop()
            elif isinstance(proc, Builtin):
                if proc.question:
                    if len(arg_value_list) == 1:
                        tos.set_msg(proc.question % arg_value_list[0], color='red')
                else:
                    tos.set_msg('What is the %s of l where l is %r' % (proc.name, args.car.value),
                                color='red')
                yield tos, stack, environments

                tos.assign_value(proc(*arg_value_list))
                tos.set_msg('===> %s' % _repr(tos.value), color='green')
                tos.mark_visited()
                yield tos, stack, environments
                stack.pop()
                environments.pop()
            else:
                raise VividRuntimeError("%s expected to be procedure" % proc)


def _require(x, predicate, msg="wrong parameters length"):
    """Signal a syntax error if predicate is false."""
    if not predicate:
        raise VividSyntaxError(str(x) + ': ' + msg)


def _find_var_in_env(var, envs):
    for i in reversed(range(len(envs))):
        if var in envs[i]:
            return envs[i][var]
    raise VividRuntimeError('unbound variable: %s' % var)


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
