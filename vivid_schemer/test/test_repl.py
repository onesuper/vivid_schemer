import unittest
from vivid_schemer.repl import Repl


class TestPlay(unittest.TestCase):

    def testNext(self):
        p = Repl()
        p.read('1')
        print([x.value for x in p])
        self.assertEqual(1, p.value)
