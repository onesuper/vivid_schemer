from vivid_schemer.sexp import SExp, SAtom
from vivid_schemer.builtin import cons
from vivid_schemer.errors import VividSyntaxError

symbol_table = {}


def new_symbol(s):
    """Find or create unique Symbol entry for str s in symbol table."""
    if s not in symbol_table:
        symbol_table[s] = SAtom(s)
    return symbol_table[s]


class Parser:
    def __init__(self, lexer):
        """tokens are feteched throw a lexer"""
        self.lexer = lexer

    def form_sexp(self):
        tok = self.lexer.tokenize()
        if str(tok) == '(':
            stack = []
            while str(self.lexer.peek()) != ')':
                stack.append(self.form_sexp())
            self.lexer.tokenize()  # reap the ')' off
            s = SExp()
            while len(stack) > 0:
                s = cons(stack.pop(), s)
            return s
        elif str(tok) == ')':
            raise VividSyntaxError('Unexpected ")" at line %d, col %d' % tok.pos)
        else:
            return new_symbol(str(tok))
