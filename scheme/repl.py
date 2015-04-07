
from parser import Parser
from lexer import Lexer
from eval import eval
from exceptions import  VividException

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
                print val.to_lisp_str()
        except VividException, e:
            print e
        


