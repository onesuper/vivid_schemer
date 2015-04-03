import sys

sys.path.append('../')

from scheme.parser import Parser
from scheme.lexer import Lexer
from scheme.exceptions import LexicalError
from scheme.exceptions import ParserError


c1 = '''

'''

c2 = '''
(a
  (b (1 2))
  (c (3 4))
  (d (5 (f (8 9))
      6))
  (e 7)
)
'''

c3 = '''
(a 1 2 () (b 9 #f))
'''


def parse_it(s):
    lexer = Lexer(s)
    parser = Parser(lexer)
    sexp = parser.form_sexp()
    print sexp
    print sexp.to_lisp_str()

for code in (c1, c2, c3):
    try:
        print '*' * 80
        print code
        parse_it(code)

    except ParserError, e:
        print e




