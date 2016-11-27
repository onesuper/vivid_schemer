import unittest
from vivid_schemer.repl import Repl


class TestRepl(unittest.TestCase):

    def testEval(self):
        p = Repl()
        p.read('1')
        self.assertEqual(1, p.eval())
