import unittest
from vivid_schemer.play import Play


class TestPlay(unittest.TestCase):

    def testNext(self):
        p = Play()
        p.parse('1')
        print([x.value for x in p])
        self.assertEqual(1, p.value)
