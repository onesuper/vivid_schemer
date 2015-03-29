#=============================================================
# An interupter for The Little Schemer in Python
# Based on Peter Norvig's lispy.py
# By onesuper
#
# The syntaxes and sementics strictly follow The Little Schemer
#==============================================================



from env import Env
from echo import Echo
from utils import ordinal, to_string
from primitives import *



isa = isinstance

# the first call to eval will use this to set up
# the global environments 
def add_globals(env):
    env.update( 
     {'+':add, '-':sub, '*':mult, '/':div,
      'add1':add1, 'sub1':sub1, '^':expt,
      'not':not_,
      '>':gt, '<':lt, '>=':gte, '<=':lte, '=':eq, 
      'cons':cons, 'car':car, 'cdr':cdr,
      'null?':is_null,
      'atom?':is_atom,
      'eq?':is_eq, 'equal?':is_equal,
      'zero?':is_zero,
      'member?':is_member,
      'number?':is_number,
      '#f':False, '#t':True, 'else':True,
      'map': map_,
      })
    return env



def eval(x, env=add_globals(Env()), lv=0):

    # deep recursion is not allowed
    if lv > 50:
        return

    "Evaluate an expression in an environment."
    "find value in env"


    if isa(x, str):               # variable reference
        return env.find(x)[x]


    elif not isa(x, list):         # constant literal
        return x

                
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
        

    elif x[0] == 'if':
        e0 = Echo("if", lv)
        e0.ask("It depends...")
        e = Echo("test", lv)
        (_, test, conseq, alt) = x
        e.ask("Is {0} true?".format(to_string(test)))
        if eval(test, env, lv+1):
            e.answer("Yes, so we do {0}.".format(to_string(conseq)))
            retval = eval(conseq, env, lv+1)
            e0.answer("It's {0}".format(to_string(retval)))
            return retval
        else:
            e.answer("No, so we do {0}.".format(to_string(alt)))
            retval = eval(alt, env, lv+1)
            e0.answer("It's {0}".format(to_string(retval)))
            return retval


    elif x[0] == 'cond':           # (cond (test conseq) (test conseq)...)
        n = 0
        e0 = Echo("cond", lv)
        e0.ask("It depends...")
        for cond in x[1:]:
            n += 1
            (test, conseq) = cond
            e = Echo("test", lv)
            e.ask("{0} quesiton: Is {1} true?".format(ordinal(n), to_string(test)))
            if eval(test, env, lv+1):    # if true
                e.answer("Yes, so we do {0}".format(to_string(conseq)))
                retval = eval(conseq, env, lv+1)
                e0.answer("It's {0}".format(to_string(retval)))
                return retval  # break out
            else:                        # if false
                e.answer("No, so we see the next question")
        # if we arrive here return NIL
        return None


    elif x[0] == 'or':           # (or exp1 exp2)   return boolean
        (_, exp1, exp2) = x
        e0 = Echo("or", lv)
        e0.ask("It depends...")
        e = Echo("or1", lv)
        e.ask("1st question: Is {0} true?".format(to_string(exp1)))
        if eval(exp1, env, lv+1):
            e.answer("yes.")
            e0.answer("It's #t")
            return True
        e.answer("nope.")
        e = Echo("or2", lv)
        e.ask("2nd question: Is {0} true?".format(to_string(exp2)))
        if eval(exp2, env, lv+1):
            e.answer("yes.")
            e0.answer("It's #t")
            return True
        e.answer("nope")
        e0.answer("Both answers are no, so it's #f")
        return False
        

    elif x[0] == 'and':           # (and exp1 exp2)   return boolean
        (_, exp1, exp2) = x
        e0 = Echo("and", lv)
        e0.ask("It depends...")
        e = Echo("and1", lv)
        e.ask("1st question: Is {0} true?".format(to_string(exp1)))
        if not eval(exp1, env, lv+1):
            e.answer("nope")
            e0.answer("It's #f")
            return False
        e.answer("yes.")
        e = Echo("and2", lv)
        e.ask("2nd question: Is {0} true?".format(to_string(exp2)))
        if not eval(exp2, env, lv+1):
            e.answer("nope")
            e0.answer("It's #f")
            return False
        e.answer("yes.")
        e0.answer("Both anwsers are yes, so It's #t")
        return True


    
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        e = Echo("define", lv)
        e.ask("define a new variable <span class=\"variable\">{0}</span>, then give it the value of <span class=\"body\">{1}</span>".format(var, to_string(exp)))
        value = eval(exp, env, lv+1)
        env[var] =  value
        e.answer("~~~")

        
    elif x[0] == 'begin':          # (begin exp*)
        e = Echo("begin", lv)
        e.ask("begin to evaluate expressions.")
        val = None
        for exp in x[1:]:
            val = eval(exp, env, lv+1)
        e.answer("Yeah, baby! It's {0}!".format(to_string(val)))
        return val

    elif x[0] == 'lambda':         # (lambda (var*) exp)
        (_, vars, exp) = x
        e = Echo("lambda", lv)
        e.ask("lambda creates a function with parameters <span class=\"parameter\">{0}</span>, <span class=\"body\">{1}</span> as body.".format(to_string(vars), to_string(exp)))
        # lv is passed via the last element of args
        retval = lambda *args: eval(exp, Env(vars, args, env), args[len(args)-1] + 1)    
        e.answer("~~~")
        return retval





    else:                          # (proc exp*)

        e = Echo("func", lv)
        args = [exp for exp in x]
        name = args.pop(0)   # get the function name in the expression
        e.ask("call <span class=\"func_name\">{0}</span> with arguments: {1}{2}".format(name, ', '.join([to_string(arg) for arg in args]), env.getOuterEnv()))
        exps = [eval(exp, env, lv+1) for exp in x]   # deeper recursion  
        proc = exps.pop(0)
        exps.append(lv)   # pass the recursion depth to the function, in 
        retval = proc(*exps)
        e.answer("you get {0}.".format(to_string(retval)))
        return retval
 

