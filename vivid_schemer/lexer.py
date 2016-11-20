from vivid_schemer.errors import VividLexicalError


class Token:
    """Lexical token remembering the position in the original code"""

    def __init__(self, literal, lineno, colno):
        self._literal = literal
        self._lineno = lineno
        self._colno = colno

    @property
    def pos(self):
        return self._lineno, self._colno

    def __repr__(self):
        return "TOKEN(literal=%s, lineno=%d, colno=%d)" % (self._literal, self._lineno, self._colno)

    def __str__(self):
        return self._literal


class Lexer:
    """The lexer only tokenize two things: string literal and parenthesis"""

    def __init__(self, text):
        self._lexdata = text
        self._lexpos = 0
        self._colno = 1
        self._lineno = 1

    def peek(self):
        return self.tokenize(True)

    def tokenize(self, readonly=False):
        import re
        while self._lexpos < len(self._lexdata):
            lex = self._lexdata[self._lexpos]
            if lex in ' \t':
                self._colno += 1
                self._lexpos += 1
                continue

            if lex == '\n':
                self._lineno += 1
                self._colno = 1
                self._lexpos += 1
                continue

            if lex in '()':
                t = Token(lex, self._lineno, self._colno)
                if readonly:
                    return t
                self._colno += 1
                self._lexpos += 1
                return t

            # not whitespace,(,)
            match = re.compile('[^\s()]*').match(self._lexdata, self._lexpos)
            if match:
                raw = match.group()
                t = Token(raw, self._lineno, self._colno)
                if readonly:
                    return t
                self._colno += len(raw)
                self._lexpos += len(raw)
                return t
        raise VividLexicalError('EOF at line %d, col %d' % (self._lineno, self._colno))


class MockLexer(object):
    def __init__(self, toks):
        self._toks = toks.split()
        self.i = 0

    def tokenize(self):
        t = Token(self._toks[self.i], 0, 0)
        self.i += 1
        return t

    def peek(self):
        t = Token(self._toks[self.i], 0, 0)
        return t
