

class SExp:
    ident = '  '
    newline = '\n'

    def __init__(self, tok, id):
        self.id = id
        self.lineno = tok.lineno
        self.colno = tok.colno
        self.children = None

    def append(self, sexp):
        """Append a sub-sexp to me"""

        if self.children is None:
            self.children = []
        self.children.append(sexp)

    def isEmptyList(self):
        return not self.children

    def treeview_str(self, depth=0):
        """
        Recursively generate a S-expression node tree.
        The nodes is indented according to its depth.
        """

        s = self.ident * depth
        s += '`-SExp %d <line:%d, col:%d>' % (self.id, self.lineno, self.colno)
        s += self.newline
        if self.children:
            for x in self.children:
                s += x.treeview_str(depth + 1)
        return s

    def lispview_str(sexp):
        """Convert the S-Exp to a Lisp-readable string."""

        s = '('
        if sexp.children:
            for x in sexp.children:
                s += x.lispview_str()
                s += ' '
        if s[-1] == ' ':
            s = s[:-1] + ')'
        else:
            s += ')'
        return s

    def __str__(self):
        return self.lispview_str()


class SAtom(SExp):
    """SAtom is a special kind of SExp but has no child."""
    def __init__(self, tok, id):
        SExp.__init__(self, tok, id)
        self.type = tok.type
        self.value = tok.value
        self.children = None

    def treeview_str(self, depth=0):
        s = self.ident * depth
        s += '`-SAtom %d <line:%d, col:%d> %s %s' % (self.id, self.lineno, self.colno, str(self.value), self.type)
        s += self.newline
        return s

    def lispview_str(self):
        return str(self.value)

    def __str__(self):
        return self.lispview_str()
