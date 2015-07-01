
from parser import Parser
from lexer import Lexer
from eval import eval
from errors import VividError
from sexp import SExp


def parse(s):
    lexer = Lexer(s)
    parser = Parser(lexer)
    sexp = parser.form_sexp()
    return sexp


def repl(prompt='vivid> '):
    while True:
        try:
            val = eval(parse(raw_input(prompt)))
            # print the value
            if isinstance(val, SExp):
                print val.lispview_str()
            else:
                print val
        except VividError, e:
            print e

repl()
