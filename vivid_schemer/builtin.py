from vivid_schemer.sexp import SExp, SAtom

from vivid_schemer.errors import VividRuntimeError

import logging

LOG = logging.getLogger(__name__)


class Builtin(object):
    """Builtin-procedure wrapper for display"""

    def __init__(self, proc, question=None):
        self._proc = proc
        self._question = question
        self._name = proc.__name__
        self._law = proc.__doc__

    @property
    def law(self):
        return self._law

    @property
    def name(self):
        return self._name

    @property
    def question(self):
        return self._question

    def __repr__(self):
        return '<Builtin: %s>' % self._name

    def __call__(self, *args):
        return self._proc(*args)


def car(x):
    """The primitive car is defined only for non-empty lists."""
    if isinstance(x, SAtom):
        x.set_msg("You cannot ask for the car of an atom.", color='red')
        LOG.warn("You cannot ask for the car of an atom.")
        return None
    elif x.isnil():
        x.set_msg("You cannot ask for the car of the empty list.", color='red')
        LOG.warn("You cannot ask for the car of the empty list.")
        return None
    x.set_msg('because %r is the first S-expression of this non-empty list.' % x.car, color='red')
    return x.car


def cdr(x):
    """The primitive cdr is defined only for non-empty lists. The cdr of any non-empty list always another list."""
    if isinstance(x, SAtom):
        x.set_msg("You cannot ask for the cdr of an atom.", color='red')
        LOG.warn("You cannot ask for the cdr of an atom.")
        return None
    if x.isnil():
        x.set_msg("You cannot ask for the cdr of a empty list.", color='red')
        LOG.warn("You cannot ask for the cdr of a empty list.")
        return None
    x.set_msg('because %r is the list l without %r.' % (x.cdr, x.car), color='red')
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
        if x.isdigits():
            x.set_msg('because it is a string of digits.', color='red')
            return True
        elif x.startswith_nondigit():
            x.set_msg('because it is a string of characters beginning with a letter.', color='red')
            return True
    x.set_msg('because %s is just a list.' % x, color='red')
    return False


def islist(x):
    if isinstance(x, SAtom):
        x.set_msg('because %s is just an atom.' % x)
        return False
    x.set_msg('because it contains S-expressions enclosed by parentheses.', color='red')
    return True


def issexp(x):
    if isinstance(x, SAtom):
        x.set_msg('because all atoms are S-expressions.', color='red')
        return True
    elif isinstance(x, SExp):
        x.set_msg('because all lists are S-expressions.', color='red')
        return True
    assert 1 == 0


def how_many_sexps(x):
    sexps = x.to_list()
    x.set_msg(', '.join([repr(s) for s in sexps]), color='red')
    return len(sexps)


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
