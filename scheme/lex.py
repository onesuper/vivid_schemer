import sys, re, types

class Token:
    def __init__(self, type):
        self.type = type
        self.value = None
        self.lineno = 0
        self.lexpos = 0
        self.lexlen = 0

    def __str__(self):
        return "TOKEN(type='%s', value='%s', lineno=%d, lexpos=%d, lexlen=%d)" \
                % (self.type, self.value, self.lineno, self.lexpos, self.lexlen)

    def __repr__(self):
        return str(self)

class LexError(Exception):
    def __init__(self, message, s):
        self.args = (message,)
        self.text = s

def t_NUMBER(t):
    t.value = int(t.value)
    return t

def t_ID(t):
    # ...
    return t

##
# @brief Regex for IDENTIFIER
letter = r'([A-Za-z])'
digit = r'([0-9])'
initial = r"(\.|\_|\+|\-|\!|\$|\%|\&|\*|\/|:|<|=|>|\?|~|\'|" + letter + r'|' + digit + r')'
subsequent = r'(' + initial + r'|#)'
ident = r'(' + initial + r'(' + subsequent + r')*)'

class Lexer:

    lexliterals = '()'
    lexignore = ' \t'
    tokens = [
            # regex,    type,   handler
            (r'\d+', 'NUMBER', t_NUMBER),
            (ident, 'ID', t_ID),
            ]

    def __init__(self):
        self.lexdata = None
        self.lexpos = 0
        self.lexlen = 0
        self.lineno = 1
        self.lexre = []
        for regex, name, func in self.tokens:
            self.lexre.append((re.compile(regex), name, func))

    def input(self, s):
        '''push a new string into lexer.'''
        self.lexdata = s
        self.lexpos = 0
        self.lexlen = len(s)
        # print("STR: ", s)

    def lexerrorf(self, t):
        '''Lex error handler'''
        return t

    def token(self):
        lexdata = self.lexdata
        lexpos = self.lexpos
        lexignore = self.lexignore

        while lexpos < self.lexlen:
            if lexdata[lexpos] in self.lexignore:
                lexpos += 1
                continue
            if lexdata[lexpos] == '\n':
                self.lineno += 1
                lexpos += 1
                continue
            for lexre, type, func in self.lexre:
                m = lexre.match(lexdata, lexpos)
                if not m: continue
                tok = Token(type)
                tok.value = m.group()
                tok.lineno = self.lineno
                tok.lexpos = lexpos
                tok.lexlen = len(tok.value)

                if not func:
                    self.lexpos = m.end()
                    return tok
                lexpos = m.end()
                self.lexpos = lexpos

                newtok = func(tok)
                if not newtok:
                    lexpos = self.lexpos
                    break
                return newtok
            else:
                # no match
                if lexdata[lexpos] in self.lexliterals:
                    tok = Token(lexdata[lexpos])
                    tok.value = lexdata[lexpos]
                    tok.lineno = self.lineno
                    tok.lexpos = lexpos
                    tok.lexlen = len(tok.value)
                    self.lexpos = lexpos + 1
                    return tok

                if self.lexerrorf:
                    tok = Token('error')
                    tok.value = self.lexdata[lexpos:]
                    tok.lineno = self.lineno
                    tok.lexpos = lexpos
                    self.lexpos = lexpos
                    newtok = self.lexerrorf(tok)
                    # No error recovery in self.lexerrorf
                    if lexpos == self.lexpos:
                        raise LexError("Scanning error. Illegal character '%s'" % (lexdata[lexpos]), lexdata[lexpos:])
                    if not newtok: continue
                    return newtok
                self.lexpos = lexpos
                # Unkown character
                raise LexError("Illegal character '%s' at index %d" % (lexdata[lexpos],lexpos), lexdata[lexpos:])
        self.lexpos = lexpos + 1
        if self.lexdata is None:
            raise RuntimeError("No input string given with input()")
        return None

