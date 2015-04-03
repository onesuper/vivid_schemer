

from exceptions import ParserError

from utils import unique_id

class SExpr:
    def __init__(self, tok):
        self.id = unique_id()()
        self.lineno = tok.lineno
        self.colno = tok.colno
        self.children = []
        self.ident = '  '
        self.newline = '\n'

    def append(self, subs):
        'append a sub-sexpr to myself'
        if self.children is None:
            self.children = []
        self.children.append(subs)

    def __str__(self, level=0):
        'recursively generate a S-expression node'
        s = self.ident * level
        s += '`-Sexp %d <line:%d, col:%d>' % (self.id, self.lineno, self.colno)
        s += self.newline
        for x in self.children:
            s += x.__str__(level + 1)
        return s


# class SNil(SExpr):
#     def __init__(self, tok):
#         SExpr.__init__(self, tok)
#         self.children = None

#     def __str__(self, level=0):
#         s = self.ident * level
#         s += '`-SNil %d <line:%d, col:%d>' % (self.id, self.lineno, self.colno)
#         s += self.newline
#         return s


class SAtom(SExpr):
    def __init__(self, tok):
        SExpr.__init__(self, tok)
        self.type = tok.type
        self.value = tok.value
        self.children = None

    def __str__(self, level=0):
        s = self.ident * level
        s += '`-SAtom %d <line:%d, col:%d> %s %s' % (self.id, self.lineno,
            self.colno, repr(self.value), self.type)
        s += self.newline
        return s


class Parser:
    def __init__(self, lexer):
        '''init a token list from a lexer'''
        self.tokens = []
        while True:
            t = lexer.next_token()
            if t is None:
                break
            self.tokens.append(t)

    # Form an S-expression from lexical tokens
    def form_sexpr(self):
        
        if len(self.tokens) == 0:
            raise ParserError("expected an (' but end of string")

        token = self.tokens.pop(0)

        if token.type == 'LPAR':  # S-expression
            L = SExpr(token)
            while self.tokens[0].type != 'RPAR':
                L.append(self.form_sexpr())
            self.tokens.pop(0) # pop off ')'
            return L
        elif token.type in ['ID', 'INT', 'BOOL']:  # Atom
            return SAtom(token)
        else:
            raise ParserError("Unrecognized token '%s' at line %d, col %d" % (token.raw, token.lineno, token.colno))
    


