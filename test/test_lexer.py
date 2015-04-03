import sys

sys.path.append('../')

from scheme.lexer import Lexer
from scheme.exceptions import LexicalError

code1 = '''
(apple
  (badboy (12 #t))
  (carry (#f 4))
  (dog (5 (fat (8 9 10abc))
      6))
  (egg 7)
)
'''



code2 = '(())))))))'
code3 = 'asdd efdf 12312 asd1223 22143a'
code4 = '*+_*/'
code5 = '''
123.12
asd_1223
10abc
9.5a 
\\u345'''

def lexit(s):
    print s
    lex = Lexer(s)
    while True:
        t = lex.next_token()
        if t is None:
            break
        print t
    print '*' * 80


lexit(code1)
lexit(code2)
lexit(code3)
lexit(code4)
try: 
    lexit(code5)
except LexicalError, e:
    print e