from vivid_schemer.sexp import SExp, SAtom

from vivid_schemer.errors import VividRuntimeError

class Builtin(object):
    """Builtin-procedure wrapper for display"""

    def __init__(self, proc, name=None):
        self._proc = proc
        if name is not None:
            self._name = name
        else:
            self._name = proc.__name__
        self._law = proc.__doc__

    @property
    def law(self):
        return self._law

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return '<Builtin: %s>' % self._name

    def __call__(self, *args):
        return self._proc(*args)


def car(x):
    """The primitive car is defined only for non-empty lists."""
    if isinstance(x, SAtom):
        raise VividRuntimeError("you cannot ask for the car of an atom.")
    elif x.isnil():
        raise VividRuntimeError("you cannot ask for the car of the empty list.")
    return x.car


def cdr(x):
    """The primitive cdr is defined only for non-empty lists. The cdr of any non-empty list always another list."""
    if isinstance(x, SAtom):
        raise VividRuntimeError("you cannot ask for the cdr of an atom")
    if x.isnil():
        raise VividRuntimeError("you cannot ask for the cdr of a empty list")
    return x.cdr


def cons(x, y):
    """The primitive cons takes two arguments. The second argument to cons must be a list. The result is a list."""
    if isinstance(y, SAtom):
        raise VividRuntimeError("the second argument to cons must be list.")
    z = SExp()
    z._car = x
    z._cdr = y
    return z


def nil():
    return SExp()


def consnil(x):
    z = SExp()
    z._car = x
    z._cdr = SExp()
    return z


def isatom(x):
    """The primitive atom? takes one argument. The argument can be any S-expression."""
    if isinstance(x, SAtom):
        if is_digit_str(x):
            return True
        elif is_letter_begin_str(x):
            return True
    x.set_msg('because %s is just a list.' % x, color='red')
    return False


def islist(x):
    if isinstance(x, SAtom):
        x.set_msg('because %s is just an atom.' % x)
        return False
    x.set_msg('because it contains S-expressions enclosed by parentheses.', color='red')
    return True


def is_letter_begin_str(x):
    import re
    if re.match(r'^[^0-9].*$', str(x)):
        x.set_msg('because it is a string of characters beginning with a letter.', color='red')
        return True
    return False


def is_digit_str(x):
    import re
    if re.match(r'^\d+$', str(x)):
        x.set_msg('because it is a string of digits.', color='red')
        return True
    return False


def isnull(x):
    """The primitive null? is defined only for lists."""
    if isinstance(x, SAtom):
        raise VividRuntimeError("you can only ask null? of a list")
    return x.isnil()


def iseq(x, y):
    """The primitive eq? takes two arguments. Each must be a non-numeric atom."""
    if isinstance(x, SAtom) and isinstance(y, SAtom) and x.value is None and y.value is None:
        return str(x) == str(y)
    else:
        raise VividRuntimeError("eq? only accepts two non-numeric atoms.")

#
# def is_equal(a, b, lv):
#     e = Echo("equal?", lv)
#     e.ask("Does {0} equal to {1}?".format(to_string(a), to_string(b)))
#     e.answer("Yes.") if a==b else e.answer("Nope.")
#     return a==b
#
#

#
#
#
# # null?
# def is_null(s, lv):
#     e = Echo("null?", lv)
#     e.ask("Is {0} an empty list?".format(to_string(s)))
#     if isa(s, list):
#         e.answer("Yes.") if s==[] else e.answer("Nope.")
#         return s==[]
#     else:
#         e.answer("No answer since you can only ask null? of a list")
#         return None
#
# # zero?
# def is_zero(n, lv):
#     e = Echo("zero?", lv)
#     e.ask("Is {0} zero?".format(to_string(n)))
#     if isa(n, int) or isa(n, float):
#         e.answer("Yes.") if n==0 else e.answer("Nope.")
#         if n==0: return True
#         else: return False
#     else:
#         e.answer("No answer since you can only ask zero? of a number")
#         return None
#
# #number?
# def is_number(s, lv):
#     e = Echo("number?", lv)
#     e.ask("Is {0} number?".format(to_string(s)))
#     if isa(s, int) or isa(s, float):
#         e.answer("Yes.")
#         return True
#     else:
#         e.answer("Nope.")
#         return False
#
# # ===========================================================
# # here we make member? a primitives behind the scenes
# # it compares anything(both number or str) in the lat to a
# # ===========================================================
# def is_member(a, lat, lv):
#     e = Echo("member?", lv)
#     e.ask("Is {0} a member of {1}?".format(to_string(a), to_string(lat)))
#     for atom in lat:
#         if a == atom:
#             e.answer("Yes.")
#             return True
#     e.answer("Nope.")
#     return False
#
#
#
# def map_(f, lat, lv):
#     e = Echo("map", lv)
#     e.ask("What's the result of mapping {0} to each element of {1}".format(to_string(f), to_string(lat)))
#     retval = []
#     for one in lat:
#         retval.append(f(one, lv))
#     e.answer("It's {0}".format(to_string(retval)))
#     return retval
