
from parser import Parser
from lexer import Lexer
from eval import eval
from errors import  VividError

def parse(s):
    lexer = Lexer(s)
    parser = Parser(lexer)
    sexp = parser.form_sexp()
    return sexp

def repl(prompt='vivid> '):
    while True:
        try:
            val = eval(parse(raw_input(prompt)))
            if val is not None:
                print repr(val)
        except VividError, e:
            print e
        


