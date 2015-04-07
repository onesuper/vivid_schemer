
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
        return False if self.children else True

    def to_lisp_str(self):
        """Convert the SExp to a Lisp-readable string."""

        s = '('
        if self.children:
            for x in self.children:
                s += x.to_lisp_str()
                s += ' '
        if s[-1] == ' ': s = s[:-1] + ')'
        else: s += ')'
        return s

    def __str__(self, depth=0):
        """
        Recursively generate a S-expression node.
        Each node is indented according to its depth.
        """

        s = self.ident * depth
        s += '`-SExp %d <line:%d, col:%d>' % (self.id, self.lineno, self.colno)
        s += self.newline
        if self.children:
            for x in self.children:
                s += x.__str__(depth + 1)
        return s

class SAtom(SExp):
    """SAtom is a special kind of SExp, which has no child."""
    
    def __init__(self, tok, id):
        SExp.__init__(self, tok, id)
        self.type = tok.type
        self.value = tok.value
        self.children = None

    def __str__(self, depth=0):
        s = self.ident * depth
        s += '`-%s %d <line:%d, col:%d> %s %s' % (
            self.__class__.__name__, self.id, self.lineno, 
            self.colno, repr(self.value), self.type)
        s += self.newline
        return s

class SSymbol(SAtom):
    def __init__(self, tok, id):
        SAtom.__init__(self, tok, id)

    def to_lisp_str(self):
        return self.value

class SInt(SAtom):
    def __init__(self, tok, id):
        SAtom.__init__(self, tok, id)

    def to_lisp_str(self):
        return str(self.value)

class SBool(SAtom):
    def __init__(self, tok, id):
        SAtom.__init__(self, tok, id)

    def to_lisp_str(self):
        return '#t' if self.value is True else '#f'

