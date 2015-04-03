

from exceptions import ParserError

from utils import unique_id

class SExp:
    ident = '  '
    newline = '\n'

    def __init__(self, tok, id):
        self.id = id
        self.lineno = tok.lineno
        self.colno = tok.colno
        self.children = None

    def append(self, sexp):
        'append a sub-sexp to me'
        if self.children is None:
            self.children = []
        self.children.append(sexp)

    def isEmptyList(self):
        if self.children:
            return False
        else:
            return True

    def to_lisp_str(self):
        'Convert the SExp to a Lisp-readable string.'
        s = '('
        if self.children:
            for x in self.children:
                s += x.to_lisp_str()
                s += ' '
        if s[-1] == ' ': s = s[:-1] + ')'
        else: s += ')'
        return s

    def __str__(self, level=0):
        'recursively generate a S-expression node'
        s = self.ident * level
        s += '`-SExp %d <line:%d, col:%d>' % (self.id, self.lineno, self.colno)
        s += self.newline
        if self.children:
            for x in self.children:
                s += x.__str__(level + 1)
        return s


class SAtom(SExp):
    def __init__(self, tok, id):
        SExp.__init__(self, tok, id)
        self.type = tok.type
        self.value = tok.value
        self.children = None

    def __str__(self, level=0):
        s = self.ident * level
        s += '`-%s %d <line:%d, col:%d> %s %s' % (
            self.__class__.__name__, self.id, self.lineno, 
            self.colno, repr(self.value), self.type)
        s += self.newline
        return s


class SSymbol(SAtom):
    def __init__(self, tok, id):
        SAtom.__init__(self, tok, id)

    def to_lisp_str(self):
        'Convert the SInt to a Lisp-readable string.'
        return self.value


class SInt(SAtom):
    def __init__(self, tok, id):
        SAtom.__init__(self, tok, id)

    def to_lisp_str(self):
        'Convert the SInt to a Lisp-readable string.'
        return str(self.value)


class SBool(SAtom):
    def __init__(self, tok, id):
        SAtom.__init__(self, tok, id)

    def to_lisp_str(self):
        'Convert the SBool to a Lisp-readable string.'
        if self.value: return '#t'
        else: return '#f'



class Parser:
    def __init__(self, lexer):
        '''init a token list from a lexer'''
        self._tokens = []
        while True:
            t = lexer.next_token()
            if t is None:
                break
            self._tokens.append(t)
        # increasing unique id for each S-expression.
        self.new_id = unique_id()

    # Form an S-expression from lexical tokens
    def form_sexp(self):
        if len(self._tokens) == 0:
            raise ParserError("expected an (' but end of string")

        tok = self._tokens.pop(0)
        if tok.type == 'LPAR':  # S-expression
            L = SExp(tok, self.new_id())
            while self._tokens[0].type != 'RPAR':
                L.append(self.form_sexp())
            self._tokens.pop(0) # pop off ')'
            return L
        elif tok.type == 'ID':
            return SSymbol(tok, self.new_id())
        elif tok.type == 'INT':
            return SInt(tok, self.new_id())
        elif tok.type == 'BOOL':
            return SBool(tok, self.new_id())
        else:
            raise ParserError("Unrecognized token '%s' at line %d, col %d" % (tok.raw, tok.lineno, tok.colno))
    
