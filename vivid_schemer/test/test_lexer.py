import unittest
from vivid_schemer.lexer import Lexer


class TestLexer(unittest.TestCase):
    def testBlanks(self):
        l = Lexer("a b  c")
        t = l.tokenize()
        self.assertEqual('a', str(t))
        self.assertEqual((1, 1), t.pos)

        t = l.tokenize()
        self.assertEqual('b', str(t))
        self.assertEqual((1, 3), t.pos)

        t = l.tokenize()
        self.assertEqual('c', str(t))
        self.assertEqual((1, 6), t.pos)

    def testNewline(self):
        l = Lexer("tom jack  \n\ntim")
        t = l.tokenize()
        self.assertEqual('tom', str(t))
        self.assertEqual((1, 1), t.pos)

        t = l.tokenize()
        self.assertEqual('jack', str(t))
        self.assertEqual((1, 5), t.pos)

        t = l.tokenize()
        self.assertEqual('tim', str(t))
        self.assertEqual((3, 1), t.pos)

    def testParen(self):
        l = Lexer("(()()")
        t = l.tokenize()
        self.assertEqual('(', str(t))
        self.assertEqual((1, 1), t.pos)

        t = l.tokenize()
        self.assertEqual('(', str(t))
        self.assertEqual((1, 2), t.pos)

        t = l.tokenize()
        self.assertEqual(')', str(t))
        self.assertEqual((1, 3), t.pos)

        t = l.tokenize()
        self.assertEqual('(', str(t))
        self.assertEqual((1, 4), t.pos)

        t = l.tokenize()
        self.assertEqual(')', str(t))
        self.assertEqual((1, 5), t.pos)

    def testPeek(self):
        l = Lexer("a b c")
        t = l.peek()
        self.assertEqual('a', str(t))
        self.assertEqual((1, 1), t.pos)

        t = l.peek()
        self.assertEqual('a', str(t))
        self.assertEqual((1, 1), t.pos)

        t = l.tokenize()
        self.assertEqual('a', str(t))
        self.assertEqual((1, 1), t.pos)

        t = l.peek()
        self.assertEqual('b', str(t))
        self.assertEqual((1, 3), t.pos)
