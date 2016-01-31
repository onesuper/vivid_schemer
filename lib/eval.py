
import logging

from env import Env
from errors import VividRuntimeError
from builtin import Builtin, car, cdr, isatom, isnull
from utils import flat_list, ordinal

LOG = logging.getLogger(__name__)
fmt = '[%(levelname)s] %(message)s (%(filename)s:%(lineno)d)'
logging.basicConfig(level=logging.INFO, format=fmt)


class Procedure(object):
    """User-defined scheme procedure"""
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __repr__(self):
        return '<Procedure %s, %s>' % (self.params, self.body)

    # def __call__(self, args):
    #     params = flat_list(self.params)
    #     args = flat_list(args)
    #
    #     print params, args
    #     if len(params) != len(args):
    #         raise VividRuntimeError('Procedure requires %d argument(s)' % len(params))
    #
    #     return evaluate(self.body, Env(params, args, self.env))


def find_var(var, envs):
    for i in reversed(range(len(envs))):
        if var in envs[i]:
            return envs[i][var]
    raise VividRuntimeError('unbound variable: %s' % var)


def evaluate(sexp, env=Env()):
    envs = []
    stack = []
    sexp.msg = "What's the value of '%s'?" % sexp
    LOG.debug(sexp.msg)
    sexp.fold_all()
    sexp.unfold()
    stack.append(sexp)
    envs.append(env)
    sexp.visited = True
    yield sexp, stack, envs

    while len(stack) != 0:
        tos = stack[-1]
        env = envs[-1]
        if isatom(tos):
            try:
                tos.value = int(tos.literal)
            except ValueError:
                try:
                    tos.value = float(tos.literal)
                except ValueError:
                    var = tos.literal
                    tos.value = find_var(var, envs)
            tos.msg = '%s' % tos.value
            stack.pop()
            envs.pop()
        elif car(tos).literal == "quote":
            tos.value = car(cdr(tos))
            tos.msg = '%s' % tos.value
            LOG.debug(tos.value)
            yield tos, stack, envs
            stack.pop()
            envs.pop()
        elif car(tos).literal == "define":
            tos.unfold_all()
            var = car(cdr(tos))
            expr = car(cdr(cdr(tos)))
            if not expr.visited:
                var.fold()
                expr.fold()
                expr.visited = True
                stack.append(expr)
                envs.append(Env())
                continue
            tos.msg = "Define a variable '%s' that equals %s" % (var, expr.value)
            var.fold()
            expr.fold()
            LOG.debug(tos.msg)
            yield tos, stack, envs
            stack.pop()
            envs.pop()
            if len(envs) > 0:  # if no outer env, just ignore it
                envs[-1][var.literal] = expr.value
        elif car(tos).literal == "lambda":
            tos.unfold_all()
            params = car(cdr(tos))
            body = car(cdr(cdr(tos)))
            params.fold()
            body.fold()
            tos.msg = "Lambda creates a procedure with params %s, and %s as body" % (params, body)
            LOG.debug(tos.msg)
            tos.value = Procedure(params, body, env)
            LOG.debug(tos.msg)
            yield tos, stack, envs
            stack.pop()
            envs.pop()
        elif car(tos).literal == "begin":  # (begin () ())
            clauses = cdr(tos)
            clauses.unfold()
            if not clauses.visited:
                y = clauses
                n = 0
                while True:
                    if isnull(y):
                        clauses.visited = True
                        tos.value = clause.value
                        break
                    n += 1
                    clause = car(y)
                    clause.fold()
                    y.unfold()
                    if not clause.visited:
                        clause.visited = True
                        clause.msg = "%s question: What's the value of '%s'?" % (ordinal(n), clause)
                        LOG.debug(clause.msg)
                        clause.unfold()
                        yield tos, stack, envs
                        stack.append(clause)
                        envs.append(Env())
                        break
                    y = cdr(y)
            else:
                tos.msg = "You get %s" % tos.value
                LOG.debug(tos.msg)
                yield tos, stack, envs
                stack.pop()
                envs.pop()
        elif car(tos).literal == "cond":  # (cond (test conseq) (test conseq)...)
            clauses = cdr(tos)
            n = 0
            while True:
                if isnull(clauses):
                    raise VividRuntimeError("Cond must take at least one true condition")
                clause = car(clauses)
                n += 1
                if not clause.visited:
                    test, conseq = car(clause), car(cdr(clause))
                    if not test.visited:
                        clause.msg = "%s question: Is %s true?" % (ordinal(n), test)
                        LOG.debug(test.msg)
                        yield clause, stack, envs
                        test.visited = True
                        stack.append(test)
                        envs.append(Env())
                        break
                    if test.value:
                        if not conseq.visited:
                            clause.msg = "Yes. You will get the value of %s" % conseq
                            LOG.debug(clause.msg)
                            conseq.visited = True
                            yield clause, stack, envs
                            stack.append(conseq)
                            envs.append(Env())
                            break
                        tos.msg = "You get %s" % conseq.value
                        LOG.debug(tos.msg)
                        tos.value = conseq.value
                        yield tos, stack, envs
                        stack.pop()
                        envs.pop()
                        break
                    else:
                        clause.visited = True
                        clause.msg = "Nope. So check the next question"
                        yield clause, stack, envs
                        LOG.debug(clause.msg)
                clauses = cdr(clauses)
        else:
            proc = car(tos)
            args = cdr(tos)

            if not proc.visited:
                proc.visited = True
                stack.append(proc)
                envs.append(Env())
                continue
            proc = proc.value

            if not args.visited:
                args.unfold()
                args.visited = True
                y = args
                while True:
                    if isnull(y):
                        break
                    arg = car(y)
                    if not arg.visited:
                        arg.visited = True
                        stack.append(arg)
                        envs.append(Env())
                    y = cdr(y)
                    y.unfold()
                continue

            args_list = flat_list(args)
            args_list = [arg.value for arg in args_list]
            args_list_str = [str(arg) for arg in args_list]

            tos.msg = "Call %s with %s." % (proc, ', '.join(args_list_str))
            LOG.debug(tos.msg)
            yield tos, stack, envs

            if isinstance(proc, Procedure):
                params_list = flat_list(proc.params)
                params_list = [parm.literal for parm in params_list]
                if len(params_list) != len(args_list):
                    raise VividRuntimeError("%s has %d parameters, %d given" %
                                            (proc, len(params_list), len(args_list)))
                e = Env(params_list, args_list)
                if not proc.body.visited:
                    proc.body.unfold()
                    proc.body.msg = "What's the value of '%s'?" % proc.body
                    LOG.debug(proc.body.msg)
                    yield proc.body, stack, envs
                    proc.body.visited = True
                    stack.append(proc.body)
                    envs.append(e)
                    continue
                tos.value = proc.body.value
                tos.msg = 'You get %s' % tos.value
                yield tos, stack, envs
                stack.pop()
                envs.pop()
            elif isinstance(proc, Builtin):
                tos.value = proc(*args_list)
                tos.msg = 'You get %s' % tos.value
                yield tos, stack, envs
                stack.pop()
                envs.pop()
            else:
                raise VividRuntimeError("%s expected to be procedure" % proc)





