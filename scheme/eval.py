
from sexp import SExp
from utils import html_spanize, num_to_ord_str, to_lisp_str
from prims import add_globals
from errors import EvalError

# for test only
from cmdline import Echo

isa = isinstance


class Env(dict):
    """Environment"""

    ident = '  '
    newline = '\n'

    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """
        Find the innermost `Env` where `var` appears.
        @param var The variable name
        @return    An `Env` that contains the variable
        """
        if var in self:
            return self
        else:
            return self.outer.find(var) if self.outer else None


    def to_pretty_str(self, depth=0):
        """
        Recursively generate the environments.
        Indented according to its depth.
        """

        s = self.ident * depth
        s += str(self)
        s += self.newline
        if self.outer:
            for x in self.outer:
                s += x.to_pretty_str(depth + 1)
        return s


    # def getOuterEnv(self):
    #     envStr = ""
    #     if self.outer is not None:
    #         for k in self.keys():
    #             envStr += ", {0} is {1}".format(k, to_string(self[k]))
    #     return envStr


def eval(sexp, env=add_globals(Env()), lv=0):
    assert(isa(sexp, SExp))  # Only an object of SExp is evaluable

    # Evaluating SAtom's values
    if sexp.isAtom():
        # Returns the true value of INT, BOOL type
        if sexp.type in ('INT', 'BOOL'):
            return sexp.value
        # variable reference
        if sexp.type == 'ID':
            id_str = sexp.value
            e = env.find(id_str)  # try to find val in the outside world
            if e is None:
                raise EvalError('unbound variable: {0}'.format(id_str))
            return e[id_str]

    # (quote body)
    if sexp.children[0].value == 'quote':
        if len(sexp.children) != 2:
            raise EvalError('quote requires 1 argument')
        (_, sbody) = sexp.children
        return sbody

    # (define var body)
    elif sexp.children[0].value == 'define':
        if len(sexp.children) != 3:
            raise EvalError('define requires 2 arguments')
        (_, svar, sbody) = sexp.children
        e = Echo("define", lv)
        e.ask("define a new variable %s and give it the value of %s" %
                (html_spanize(to_lisp_str(svar), 'variable'),
                 html_spanize(to_lisp_str(sbody), 'body')))
        env[svar.value] = eval(sbody, env, lv+1)
        e.answer("define complete")

    # (lambda params body)
    elif sexp.children[0].value == 'lambda':
        if len(sexp.children) != 3:
            raise EvalError('lambda requires 2 arguments')
        (_, sparams, sbody) = sexp.children
        e = Echo("lambda", lv)
        e.ask("lambda creates a function with params %s, and %s as body" %
                (html_spanize(to_lisp_str(sparams), 'parameter'),
                 html_spanize(to_lisp_str(sbody), 'body')))

        # construct the parameter list like: (a b c) and check the type
        params = []
        for i, param in enumerate(sparams.children):
            if not isa(param, SSymbol):
                raise EvalError('the %s parameter expected to be symbol' % num_to_ord_str(i+1))
            params.append(param.value)

        # create a anonymous function with Python's lambda function
        # lv is passed via the last element of args
        retval = lambda *args: eval(sbody, Env(params, args, env), args[len(args)-1] + 1)
        e.answer("function %s created" % str(retval))
        return retval

    # (if test conseq alt)
    elif sexp.children[0].value == 'if':
        if len(sexp.children) != 4:
            raise EvalError('if requires 3 arguments')
        (_, test, conseq, alt) = sexp.children
        e0 = Echo("if", lv)
        e0.ask("It depends...")
        e = Echo("test", lv)
        e.ask("Is %s true?" % to_lisp_str(test))
        if eval(test, env, lv+1):
            e.answer("Yes, so we do %s" % to_lisp_str(conseq))
            retval = eval(conseq, env, lv+1)
        else:
            e.answer("No, so we do %s" % to_lisp_str(alt))
            retval = eval(alt, env, lv+1)
        e0.answer("It's %s" % to_lisp_str(retval))
        return retval

    # (func_name func_args)
    else:
        e = Echo("func", lv)
        func_name = sexp.children[0]
        func_args = sexp.children[1:]
        e.ask("call %s with arguments: %s" % (html_spanize(to_lisp_str(func_name), 'name'), ', '.join([to_lisp_str(arg) for arg in func_args])))
        # eval all arguments
        func_args = [eval(exp, env, lv+1) for exp in sexp.children[1:]]

        func_name = eval(func_name)

        func_args.append(lv)   # pass the recursion depth to the function, in
        assert hasattr(func_name, '__call__')
        retval = func_name(*func_args)
        e.answer("you get %s" % to_lisp_str(retval))
        return retval
