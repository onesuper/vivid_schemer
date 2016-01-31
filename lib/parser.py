
from sexp import SExp, SAtom
from builtin import cons
from errors import VividSyntaxError


class Parser:
    def __init__(self, lexer):
        """tokens are feteched throw a lexer"""
        self.lexer = lexer

    def form_sexp(self):
        tok = self.lexer.tokenize()
        if tok.literal == '(':
            stack = []
            while self.lexer.peek().literal != ')':
                stack.append(self.form_sexp())
            self.lexer.tokenize()  # reap the ')' off
            s = SExp()
            while len(stack) > 0:
                s = cons(stack.pop(), s)
            return s
        elif tok.literal == ')':
            raise VividSyntaxError('Unexpected ")" at line %d, col %d' % (tok.lineno, tok.colno))
        else:
            return SAtom(tok.literal)


