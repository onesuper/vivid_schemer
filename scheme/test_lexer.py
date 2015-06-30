import unittest
import lexer

class TestLex(unittest.TestCase):

    def setUp(self):
        pass

    def test_bool(self):
        code = '#true #t #false #f'
        lex = lexer.Lexer(code)

        tok = lex.next_token()
        self.assertEqual(tok.value, True)
        self.assertEqual(tok.raw, '#true')
        tok = lex.next_token()
        self.assertEqual(tok.value, True)
        self.assertEqual(tok.raw, '#t')

        tok = lex.next_token()
        self.assertEqual(tok.value, False)
        self.assertEqual(tok.raw, '#false')
        tok = lex.next_token()
        self.assertEqual(tok.value, False)
        self.assertEqual(tok.raw, '#f')

    def test_string(self):
        code = '"hello" "hello\\"" "hello\\\\" "hello \\ \t \n \tworld"'
        print(code)
        lex = lexer.Lexer(code)

        tok = lex.next_token()
        self.assertEqual(tok.raw, '"hello"')
        self.assertEqual(tok.value, 'hello')

        tok = lex.next_token()
        self.assertEqual(tok.raw, '"hello\\""')
        self.assertEqual(tok.value, 'hello"')

        tok = lex.next_token()
        self.assertEqual(tok.raw, '"hello\\\\"')
        self.assertEqual(tok.value, 'hello\\')

        tok = lex.next_token()
        self.assertEqual(tok.raw, '"hello \\ \t \n \tworld"')
        self.assertEqual(tok.value, 'hello world')

    def test_identifier(self):
        code = "define\\'@._+-!$*/:<=>?~\\\\"
        tok = lexer.Lexer(code).next_token()
        self.assertEqual(tok.raw, code)

    def test_int(self):
        code1 = '9'
        tok = lexer.Lexer(code1).next_token()
        self.assertEqual(tok.value, 9)

        code2 = '9 3'
        tok = lexer.Lexer(code2).next_token()
        self.assertEqual(tok.value, 9)

    def test_float(self):
        code1 = '9.52 a'
        tok = lexer.Lexer(code1).next_token()
        self.assertEqual(tok.value, 9.52)

        code2 = '9.5a'
        tok = lexer.Lexer(code2).next_token()
        self.assertEqual(tok.value, code2)

    def test_comment(self):
        code1 = ';;sdafsdf\n'
        tok = lexer.Lexer(code1).next_token()
        self.assertEqual(tok.value, None)
