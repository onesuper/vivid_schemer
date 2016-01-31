import unittest
from lib.lexer import Lexer


class TestLexer(unittest.TestCase):

    def testBlanks(self):
        l = Lexer("a b  c")
        t = l.tokenize()
        self.assertEqual('a', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(1, t.colno)

        t = l.tokenize()
        self.assertEqual('b', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(3, t.colno)

        t = l.tokenize()
        self.assertEqual('c', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(6, t.colno)

    def testNewline(self):
        l = Lexer("tom jack  \n\ntim")
        t = l.tokenize()
        self.assertEqual('tom', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(1, t.colno)

        t = l.tokenize()
        self.assertEqual('jack', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(5, t.colno)

        t = l.tokenize()
        self.assertEqual('tim', t.literal)
        self.assertEqual(3, t.lineno)
        self.assertEqual(1, t.colno)

    def testParen(self):
        l = Lexer("(()()")
        t = l.tokenize()
        self.assertEqual('(', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(1, t.colno)

        t = l.tokenize()
        self.assertEqual('(', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(2, t.colno)

        t = l.tokenize()
        self.assertEqual(')', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(3, t.colno)

        t = l.tokenize()
        self.assertEqual('(', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(4, t.colno)

        t = l.tokenize()
        self.assertEqual(')', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(5, t.colno)

    def testPeek(self):
        l = Lexer("a b c")
        t = l.peek()
        self.assertEqual('a', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(1, t.colno)

        t = l.peek()
        self.assertEqual('a', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(1, t.colno)

        t = l.tokenize()
        self.assertEqual('a', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(1, t.colno)

        t = l.peek()
        self.assertEqual('b', t.literal)
        self.assertEqual(1, t.lineno)
        self.assertEqual(3, t.colno)
