
from sexp import SExp, SSymbol, SInt, SBool
from utils import html_spanize
from builtins import add_builtins
from exceptions import WrongParamsError, SyntaxError

# for test only
from cmd import Echo 

isa = isinstance

class Env(dict):
    """Environment"""
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """
        Find the innermost `Env` where `var` appears.
        @param var The variable name
        @return    An `Env` that contains the variable
        """
        return self if var in self else self.outer.find(var)

    # def getOuterEnv(self):
    #     envStr = ""
    #     if self.outer is not None:
    #         for k in self.keys():
    #             envStr += ", {0} is {1}".format(k, to_string(self[k]))
    #     return envStr
    

def eval(sexp, env=Env(), lv=0):
    """

    """

    if sexp.isEmptyList():
        raise SyntaxError('first empty: %s' % sexp.to_lisp_str(), sexp.lineno, sexp.colno)

    # (quote exp)
    if sexp.children[0].value == 'quote':
        if len(sexp.children) != 2:
            raise WrongParamsError('quote', 1, sexp.lineno, sexp.colno)
        (_, exp) = sexp.children
        return exp

    # (define var exp)
    elif sexp.children[0].value == 'define':
        if len(sexp.children) != 3:
            raise WrongParamsError('define', 2, sexp.lineno, sexp.colno)
        (_, var, exp) = sexp.children
        e = Echo("define", lv)
        e.ask("define a new variable %s and give it the value of %s" %
                (html_spanize(var.to_lisp_str(), 'variable'),
                 html_spanize(exp.to_lisp_str(), 'body')))
        env[var] = eval(exp, env, lv+1)
        e.answer("define complete")

    # (lambda params body)
    elif sexp.children[0].value == 'lambda':
        if len(sexp.children) != 3:
            raise WrongParamsError('lambda', 2, sexp.lineno, sexp.colno)
        (_, params, exp) = sexp
        e = Echo("lambda", lv)
        e.ask("lambda creates a function with params %s, and %s as body" % 
                (html_spanize(params.to_lisp_str(), 'parameter'),
                 html_spanize(body.to_lisp_str()), 'body'))
        
        # create a anonymous function with Python's lambda function
        # lv is passed via the last element of args        
        retval = lambda *args: eval(exp, Env(params, args, env), args[len(args)-1] + 1)    
        e.answer("function %s created", str(retval))
        return retval

    # (if test conseq alt)
    elif sexp.children[0].value == 'if':
        if len(sexp.children) != 4:
            raise WrongParamsError('if', 3, sexp.lineno, sexp.colno)
        (_, test, conseq, alt) = x.children
        e0 = Echo("if", lv)
        e0.ask("It depends...")
        e = Echo("test", lv)
        e.ask("Is %s true?" % test.to_lisp_str())
        if eval(test, env, lv+1):
            e.answer("Yes, so we do %s" % conseq.to_lisp_str())
            retval = eval(conseq, env, lv+1)
        else:
            e.answer("No, so we do %s" % alt.to_lisp_str())
            retval = eval(alt, env, lv+1)        
        e0.answer("It's %s" % retval.to_lisp_str())
        return retval

    # (func_name func_args)
    else: 
        e = Echo("func", lv)
        func_name = sexp.children[0]
        func_args = sexp.children[1:]
        e.ask("call %s with arguments: %s" % 
                (html_spanize(func_name.to_lisp_str(), 'name'), 
                 ', '.join([arg.to_lisp_str() for arg in func_args])))
        # eval all arguments
        func_args = [eval(exp, env, lv+1) for exp in sexp.children[1:]]   
        func_name = eval(func_name)
        func_args.append(lv)   # pass the recursion depth to the function, in
        assert hasattr(obj, '__call__')
        retval = func_name(*func_args)
        e.answer("you get %s" % retval.to_lisp_str())
        return retval




 

