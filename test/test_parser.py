import unittest
from lib.parser import Parser
from lib.lexer import MockLexer
from lib.errors import VividSyntaxError


class TestParser(unittest.TestCase):

    def test(self):
        p = Parser(MockLexer("( )"))
        self.assertEqual('()', p.form_sexp().pairstr())

        p = Parser(MockLexer("a"))
        self.assertEqual('a', p.form_sexp().pairstr())

        p = Parser(MockLexer("( a )"))
        self.assertEqual('(a . ())', p.form_sexp().pairstr())

        p = Parser(MockLexer("( (  ) )"))
        self.assertEqual('(() . ())', p.form_sexp().pairstr())

        p = Parser(MockLexer("( a ( ) )"))
        sexp = p.form_sexp()

        p = Parser(MockLexer("( a b c )"))
        self.assertEqual('(a . (b . (c . ())))', p.form_sexp().pairstr())

        p = Parser(MockLexer("( a ( b ) )"))
        self.assertEqual('(a . ((b . ()) . ()))', p.form_sexp().pairstr())

        p = Parser(MockLexer("( a b ) ) c )"))
        self.assertEqual('(a . (b . ()))', p.form_sexp().pairstr())

        p = Parser(MockLexer("( ( b ) ( c ) )"))
        # ((b . Nil) . ((c . Nil) . Nil))
        self.assertEqual('((b . ()) . ((c . ()) . ()))', p.form_sexp().pairstr())

        p = Parser(MockLexer("( d ( b a ) c )"))
        # (d . ((b . (a . Nil)) . (c . Nil)))
        self.assertEqual('(d . ((b . (a . ())) . (c . ())))', p.form_sexp().pairstr())

        p = Parser(MockLexer(")"))
        with self.assertRaises(VividSyntaxError) as cm:
            p.form_sexp()
        self.assertEqual('SyntaxError: Unexpected ")" at line 0, col 0', cm.exception.message)