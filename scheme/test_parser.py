

from parser import Parser
from lexer import Lexer
from eval import eval
from errors import VividError

def parse(s):
    lexer = Lexer(s)
    parser = Parser(lexer)
    sexp = parser.form_sexp()
    return sexp

def parse_it(prompt='parser> '):
    while True:
            sexp = parse(raw_input(prompt))
            print sexp
        

parse_it()