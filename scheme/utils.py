

isa = isinstance


def to_lisp_str(sexp):
    """Convert the SExp to a Lisp-readable string."""
    if isa(sexp, int):
        return str(sexp)

    if sexp.isAtom():
        return str(sexp.value)

    s = '('
    if sexp.children:
        for x in sexp.children:
            s += to_lisp_str(x)
            s += ' '
    if s[-1] == ' ':
        s = s[:-1] + ')'
    else:
        s += ')'
    return s


def unique_id():
    """
    Use to assign unique id for each atom
    """
    count = [0]
    def incr():
        count[0] += 1
        return count[0]
    return incr


def num_to_ord_str(n):
    """
    Returns an ordinal number decorated string (e.g. '2nd')
    @param n  A integer number
    """
    if 4 <= n <= 20 or 24 <= n <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][n % 10 - 1]
    return str(n)+suffix


def html_spanize(s, classname):
    return '<span class=\"%s\">%s</span>' % (classname, s)
