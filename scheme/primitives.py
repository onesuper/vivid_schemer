#=============================================================
# An interupter for The Little Schemer in Python
# Based on Peter Norvig's lispy.py
# By onesuper
#
# The syntaxes and sementics strictly follow The Little Schemer
#==============================================================


#=======================================================
# all the native primitives are defined in this file
#=======================================================



from utils import to_string
from echo import Echo

#======================================================
# arithmetic 
#======================================================
def add(a, b, lv):
    e = Echo("add", lv)
    e.ask("What's the result of {0} + {1}?".format(to_string(a), to_string(b)))
    e.answer("{0}.".format(a+b))
    return a+b


def sub(a, b, lv):
    e = Echo("sub", lv)
    e.ask("What's the result of {0} - {1}?".format(to_string(a), to_string(b)))
    e.answer("{0}.".format(a-b))
    return a-b


def mult(a, b, lv):
    e = Echo("mult", lv)
    e.ask("What's the result of {0} * {1}?".format(to_string(a) ,to_string(b)))
    e.answer("{0}.".format(a*b))
    return a*b


def div(a, b, lv):
    e = Echo("div", lv)
    e.ask("What's the result of {0} / {1}?".format(to_string(a), to_string(b)))
    if b == 0:
        raise ZeroDivisionError
    e.answer("{0}.".format(a/b))
    return a/b


def add1(n, lv):
    e = Echo("add1", lv)
    e.ask("What is the result of adding 1 to {0}?".format(to_string(n)))
    e.answer("{0}.".format(n+1))
    return n+1


def sub1(n, lv):
    e = Echo("sub1", lv)
    e.ask("What is the result of subtracting 1 from {0}?".format(to_string(n)))
    e.answer("{0}.".format(n-1))
    return n-1


def expt(n, m, lv):
    e = Echo("expt", lv)
    e.ask("What is rasing {0} to the power of {1}".format(to_string(n), to_string(m)))
    e.answer("{0}.".format(n**m))
    return n**m

#==========================================================
# List Operation
#==========================================================
def car(x, lv):
    e = Echo("car", lv)
    e.ask("What's car of {0}?".format(to_string(x)))
    if isa(x, str):
        e.answer("No answer, because you cannot ask for the car of an atom.")
        return None
    elif isa(x, list):
        if x == []:
            e.answer("No answer, because you cannot ask for the car of the empty list.")
            return None
        else:
            e.answer("{0}.".format(to_string(x[0])))
            return x[0]
    else:
         e.answer("No answer, because car is only for non-empty lists.")
         return None
    



def cdr(x, lv):
    e = Echo("cdr", lv)
    e.ask("What's cdr of {0}?".format(to_string(x)))
    if isa(x, str):
        e.answer("No answer, since you cannot ask for the cdr of an atom.")
        return None
    elif isa(x, list):
        if x == []:
            e.answer("No answer, since you cannot ask for the cdr of the empty list.")
            return None
        else:
            e.answer("{0}.".format(to_string(x[1:])))
            return x[1:]
    else:
        e.answer("No answer, because cdr is only for non-empty lists.")
        return None

def cons(x, y, lv):
    e = Echo("cons", lv)
    e.ask("What's cons of {0} and {1}?".format(to_string(x), to_string(y)))
    if isa(y, list):
        e.answer("{0}.".format(to_string([x]+y)))
        return [x]+y
    else: 
        e.answer("No answer, since the second argument to cons must be list.")
        return None


#=============================================================
# comparation
#=============================================================
def gt(a, b, lv):
    e = Echo("gt", lv)
    e.ask("Is {0} greater than {1}?".format(a, b))
    e.answer("Yes.") if a > b else e.answer("Nope.")
    return a > b


def gte(a, b, lv):
    e = Echo("gte", lv)
    e.ask("Is {0} greater or equal than {1}?".format(a, b))
    e.answer("Yes.") if a >= b else e.answer("Nope.")
    return a >= b


def lt(a, b, lv):
    e = Echo("lt", lv)
    e.ask("Is {0} less than {1}?".format(a, b))
    e.answer("Yes.") if a < b else e.answer("Nope.")
    return a < b


def lte(a, b, lv):
    e = Echo("lte", lv)
    e.ask("Is {0} less or equal than {1}?".format(a, b))
    e.answer("Yes.") if a <= b else e.answer("Nope")
    return a <= b


def eq(a, b, lv):
    e = Echo("eq", lv)
    e.ask("Is {0} = {1}?".format(a, b))
    e.answer("Yes.") if a == b else e.answer("Nope.")
    return a == b


#=============================================================
# bool operator
#=============================================================
def not_(s, lv):
    e = Echo("not", lv)
    e.ask("What's opposite to {0}?".format(to_string(s)))
    e.answer("It's {0}".format(not s))
    return not s





#=============================================================
# eq?
# number constants are not considered here
# but in practice, some numbers my be arguments of eq?
#=============================================================
def is_eq(a, b, lv):
    e = Echo("eq?", lv)
    e.ask("Does {0} eq to {1}?".format(to_string(a), to_string(b)))
    if isa(a, str) and isa(b, str):
        e.answer("Yes.") if a==b else e.answer("Nope.")
        return a==b
    else:
        e.answer("No answer because eq? only accepts two non-numeric atoms.")
        return None


def is_equal(a, b, lv):
    e = Echo("equal?", lv)
    e.ask("Does {0} equal to {1}?".format(to_string(a), to_string(b)))
    e.answer("Yes.") if a==b else e.answer("Nope.")
    return a==b


# all numbers are atom
# atom?
def is_atom(s, lv):
    e = Echo("atom?", lv)
    e.ask("Is {0} an atom?".format(to_string(s)))
    e.answer("Yes.") if isa(s, str) or isa(s, int) or isa(s, float) else e.answer("Nope.")
    return isa(s, str) or isa(s, int) or isa(s, float)



# null?
def is_null(s, lv):
    e = Echo("null?", lv)
    e.ask("Is {0} an empty list?".format(to_string(s)))
    if isa(s, list):
        e.answer("Yes.") if s==[] else e.answer("Nope.")
        return s==[]
    else: 
        e.answer("No answer since you can only ask null? of a list")
        return None

# zero?
def is_zero(n, lv):
    e = Echo("zero?", lv)
    e.ask("Is {0} zero?".format(to_string(n)))
    if isa(n, int) or isa(n, float):
        e.answer("Yes.") if n==0 else e.answer("Nope.")
        if n==0: return True
        else: return False
    else:
        e.answer("No answer since you can only ask zero? of a number")
        return None

#number?
def is_number(s, lv):
    e = Echo("number?", lv)
    e.ask("Is {0} number?".format(to_string(s)))
    if isa(s, int) or isa(s, float):
        e.answer("Yes.")
        return True
    else:
        e.answer("Nope.")
        return False

# ===========================================================
# here we make member? a primitives behind the scenes
# it compares anything(both number or str) in the lat to a 
# ===========================================================
def is_member(a, lat, lv):
    e = Echo("member?", lv)
    e.ask("Is {0} a member of {1}?".format(to_string(a), to_string(lat)))
    for atom in lat:
        if a == atom:
            e.answer("Yes.")
            return True
    e.answer("Nope.")
    return False



def map_(f, lat, lv):
    e = Echo("map", lv)
    e.ask("What's the result of mapping {0} to each element of {1}".format(to_string(f), to_string(lat)))
    retval = []
    for one in lat:
        retval.append(f(one, lv))
    e.answer("It's {0}".format(to_string(retval)))
    return retval
