
from exceptions import LexicalError
import re

class Token:
    def __init__(self, type):
        self.type = type    # string e.g. 'INT'
        self.raw = None     # string e.g. 'name123'
        self.value = None   # python type, e.g. True
        self.lineno = 0
        self.colno = 0

    def __str__(self):
        return "TOKEN(type='%s', value=%s, lineno=%d, colno=%d)" \
                % (self.type, repr(self.value), self.lineno, self.colno)

##
# @brief Handlers to set the value of a type from its raw data
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

class Lexer:
    letter = r'([A-Za-z])'
    digit = r'([0-9])'
    initial = r'(\.|\_|\+|\-|\!|\$|\%|\&|\*|\/|:|<|=|>|\?|~|\'|' + letter + r'|' + digit + r')'
    subsequent = r'(' + initial + r'|#)'

    # Regexes
    integer_rex = re.compile(r'\d+')
    ident_rex = re.compile(r'(' + initial + r'(' + subsequent + r')*)')
    boolean_rex = re.compile(r'\#t|\#f')

    tokens = [
        # regex,    type,   handler
        (integer_rex,   'INT',  t_INT),
        (ident_rex,     'ID',   t_ID),
        (boolean_rex,   'BOOL', t_BOOL),
    ]

    def __init__(self, s):
        '''init a lexer from a string.'''
        self.lexdata = s
        self.lexpos = 0
        self.colno = 0
        self.lineno = 1
        self.lexre = []
        for regex, name, func in self.tokens:
            self.lexre.append((regex, name, func))

    # Get next token from the lexer (move the lexpos)
    def next_token(self):
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
            # attempts to match the LPAR/RPAR             
            if self.lexdata[lexpos] in '()':
                if self.lexdata[lexpos] == '(':
                    tok = Token('LPAR')
                else:
                    tok = Token('RPAR')
                tok.raw = self.lexdata[lexpos] 
                tok.value = None
                tok.lineno = self.lineno
                tok.colno = self.colno
                self.colno += 1
                self.lexpos = lexpos + 1
                return tok
            # attempts to match a regex pattern
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

        
    

