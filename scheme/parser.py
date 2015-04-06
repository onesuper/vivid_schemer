
from sexp import SExp, SSymbol, SInt, SBool
from exceptions import ParserError
from utils import unique_id

class Parser:
    def __init__(self, lexer):
        """init a token list from a lexer"""
        self._tokens = []
        while True:
            t = lexer.next_token()
            if t is None:
                break
            self._tokens.append(t)
        self.new_id = unique_id() # increasing unique id for each S-expression.

    def form_sexp(self):
        """Form an S-expression from lexical tokens"""
        
        if len(self._tokens) == 0:
            raise ParserError("expected an (' but end of string")

        tok = self._tokens.pop(0)
        if tok.value == '(':  # S-expression
            L = SExp(tok, self.new_id())
            while self._tokens[0].value != ')':
                L.append(self.form_sexp())
            self._tokens.pop(0) # delete ')'
            return L
        elif tok.type == 'ID':
            return SSymbol(tok, self.new_id())
        elif tok.type == 'INT':
            return SInt(tok, self.new_id())
        elif tok.type == 'BOOL':
            return SBool(tok, self.new_id())
        else:
            raise ParserError("Unrecognized token '%s' at line %d, col %d" % 
                (tok.raw, tok.lineno, tok.colno))
    
