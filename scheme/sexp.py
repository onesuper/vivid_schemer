


class SExp:
    ident = '  '
    newline = '\n'

    def __init__(self, tok, id):
        self.id = id
        self.lineno = tok.lineno
        self.colno = tok.colno
        self.children = None
        self.isLeaf = False

    def append(self, sexp):
        """Append a sub-sexp to me"""

        if self.children is None:
            self.children = []
        self.children.append(sexp)

    def isEmptyList(self):
        return False if self.children else True

    def isAtom(self):
        return self.isLeaf

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
        self.isLeaf = True

    def __str__(self, depth=0):
        s = self.ident * depth
        s += '`-SAtom %d <line:%d, col:%d> %s %s' % (self.id, self.lineno, self.colno, str(self.value), self.type)
        s += self.newline
        return s
