
from errors import VividLexicalError

class Token:
    """Lexical token remembering the position in the original code"""
    def __init__(self, literal, lineno, colno):
        self.literal = literal
        self.lineno = lineno
        self.colno = colno

    def __str__(self):
        return "TOKEN(literal=%s, lineno=%d, colno=%d)" % (self.literal, self.lineno, self.colno)


class Lexer:
    """The lexer only tokenize two things: string literal and parenthis"""
    def __init__(self, text):
        self.lexdata = text
        self.lexpos = 0
        self.colno = 1
        self.lineno = 1

    def peek(self):
        return self.tokenize(True)

    def tokenize(self, readonly=False):
        import re
        while self.lexpos < len(self.lexdata):
            lex = self.lexdata[self.lexpos]
            if lex in ' \t':
                self.colno += 1
                self.lexpos += 1
                continue

            if lex == '\n':
                self.lineno += 1
                self.colno = 1
                self.lexpos += 1
                continue

            if lex in '()':
                t = Token(lex, self.lineno, self.colno)
                if readonly:
                    return t
                self.colno += 1
                self.lexpos += 1
                return t

            # not whitespace,(,)
            match = re.compile('[^\s\(\)]*').match(self.lexdata, self.lexpos)
            if match:
                raw = match.group()
                t = Token(raw, self.lineno, self.colno)
                if readonly:
                    return t
                self.colno += len(raw)
                self.lexpos += len(raw)
                return t
        raise VividLexicalError('EOF at line %d, col %d' % (self.lineno, self.colno))


class MockLexer(object):
    def __init__(self, toks):
        self.toks = toks.split()
        self.i = 0

    def tokenize(self):
        t = Token(self.toks[self.i], 0, 0)
        self.i += 1
        return t

    def peek(self):
        t = Token(self.toks[self.i], 0, 0)
        return t
