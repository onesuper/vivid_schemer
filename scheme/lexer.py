
from exceptions import LexicalError

class Token:
    """Lexical token remembering the position in the original code"""
    def __init__(self, type):
        self.type = type    # string e.g. 'INT'
        self.raw = None     # string e.g. 'name123'
        self.value = None   # python type, e.g. True
        self.lineno = 0
        self.colno = 0

    def __str__(self):
        return "TOKEN(type='%s', value=%s, lineno=%d, colno=%d)" \
                % (self.type, repr(self.value), self.lineno, self.colno)

# Handlers to set the value of a type from its raw data
def t_INT(t):
    t.value = int(t.raw)
    return t

def t_ID(t):
    t.value = t.raw
    return t

def t_BOOL(t):
    if t.raw == '#t':
        t.value = True
    else:
        t.value = False
    return t

def t_PAR(t):
    t.value = t.raw
    return t


# Regular expressions to form identifier
letter = '([A-Za-z])'
digit = '([0-9])'
initial = '(\.|\_|\+|\-|\!|\$|\%|\&|\*|\/|:|<|=|>|\?|~|\'|' + letter + '|' + digit + ')'
subsequent = '(' + initial + '|#)'


class Lexer:

    """
    Lexer define a bunch of regex string to be used by other module (e.g. highlighter).
    The tokens are fetched one-by-one by calling `next_token()`
    """

    KEYWORD = '''\bdefine\b|\bbegin\b|\blambda\b|\bquote\b|\bcond\b|\bor\b|\band\b|
              \belse\b|\beq\?\b|\batom\?\b|\bnull\?\b|\bzero\?\b|\bcar
              \b|\bcdr\b|\bcons\b|\bif\b|\bmap\b'''
    INT  = '\d+'
    ID   = '(' + initial + '(' + subsequent + ')*)'
    BOOL = '#t|#f'
    PAR  = '\(|\)'

    def __init__(self, s):
        """init a lexer from a string(the code to be executed)."""

        import re

        self.lexdata = s
        self.lexpos = 0
        self.colno = 0
        self.lineno = 1
        self.lexre = []
        self.tokens = [
            # regex, type,  handler
            (self.INT,   'INT',  t_INT),
            (self.ID,    'ID',   t_ID),
            (self.BOOL,  'BOOL', t_BOOL),
            (self.PAR,   'PAR',  t_PAR),
        ]
        for regex, name, func in self.tokens:
            self.lexre.append((re.compile(regex), name, func))

    def next_token(self):
        """Get next token from the lexer (move the lexpos)"""

        lexpos = self.lexpos
        while lexpos < len(self.lexdata):
            if self.lexdata[lexpos] in ' \t':
                self.colno += 1
                lexpos += 1
                continue
            if self.lexdata[lexpos] == '\n':
                self.lineno += 1
                self.colno = 0
                lexpos += 1
                continue
            for lexre, type, setvalue in self.lexre:
                match = lexre.match(self.lexdata, lexpos)
                if match:
                    tok = Token(type)
                    tok.raw = match.group()  # raw value -> matched str
                    tok.lineno = self.lineno
                    tok.colno = self.colno
                    self.colno += len(tok.raw)                    
                    self.lexpos = lexpos + len(tok.raw) 
                    tok = setvalue(tok)    # set the value 
                    return tok
            else:
                raise LexicalError("Illegal character '%s' at line: %d, col: %d " %
                    (self.lexdata[lexpos], self.lineno , self.colno))
