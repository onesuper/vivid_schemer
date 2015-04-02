#=============================================================
# An interupter for The Little Schemer in Python
#
# The syntaxes and sementics strictly follow The Little Schemer
#==============================================================

import lex

def counter(start_at = 0):
    count = [start_at]
    def incr():
        count[0] += 1
        return count[0]
    return incr

new_id = counter()

class SExpr:
    value = None
    lineno = 0
    span = None
    children = None

    def __init__(self, tok):
        if tok.type == '(':
            self.id = new_id()
            self.children = []
            self.span = (tok.lexpos, tok.lexlen)
        else:
            self.id = 0
            self.value = tok.value
            self.lineno = tok.lineno
            self.span = (tok.lexpos, tok.lexpos + tok.lexlen)

    def append(self, sexpr):
        if self.children is None:
            self.children = []
        self.children.append(sexpr)

    def complete(self, tok):
        self.span = (self.span[0], tok.lexpos + tok.lexlen)

    def to_list(self):
        if self.children is None:
            return self.value
        else:
            return [x.to_list() for x in self.children]

    def __str__(self):
        return str(self.value if self.isAtom() else self.children)

    def __repr__(self):
        return repr(self.value if self.isAtom() else self.children)

    def isAtom(self):
        return self.children is None

    def isList(self):
        return isinstance(self.children, list)

    def isEmptyList(self):
        if self.isList() and len(self.children) == 0:
            return True
        else:
            return False

class SyntaxError(Exception):
    def __init__(self, message):
        self.args = (message)

class Parser:

    lookup = None
    ast_tree = None

    def __init__(self, lexer):
        self.lexer = lexer
        self.__move()

    def __move(self):
        self.lookup = self.lexer.token()

    def __match(self, type):
        if self.lookup.type is type:
            self.__move()
        else:
            raise SyntaxError("Error at %s" % (str(self.lookup)))

    def yacc(self):
        L = []
        while self.lookup:
            s = self.__form()
            if s is None:
                break
            L.append(s)
        if len(L) == 1:
            self.ast_tree = L[0]
        else:
            self.ast_tree = L

    def __form(self):
        if self.lookup.type == '(':
            L = SExpr(self.lookup)
            self.__match('(')
            while self.lookup.type != ')':
                if self.lookup.type == '(':
                    s = self.__form()
                    L.append(s)
                else:
                    L.append(SExpr(self.lookup))
                    self.__move()
            L.complete(self.lookup)
            self.__match(')')
            return L
        elif self.lookup.type in ['ID', 'NUMBER']:
            sexpr = SExpr(self.lookup)
            return sexpr
        else:
            raise SyntaxError("Error at %s" % (str(self.lookup)))

def parse(s):
    lexer = lex.Lexer()
    lexer.input(s)
    parser = Parser(lexer)
    parser.yacc()
    return parser.ast_tree
