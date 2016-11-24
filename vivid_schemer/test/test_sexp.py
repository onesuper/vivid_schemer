import unittest
from vivid_schemer.sexp import SExp, SAtom
from vivid_schemer.builtin import cons


class TestSExp(unittest.TestCase):
    def setUp(self):
        self.nil = SExp()
        self.assertFalse(isinstance(self.nil, SAtom))
        self.a = SAtom('a')
        self.assertTrue(isinstance(self.a, SAtom))
        self.b = SAtom('b')
        self.c = SAtom('c')
        self.d = SAtom('d')
        self.al = cons(self.a, SExp())
        self.bl = cons(self.b, SExp())
        self.cl = cons(self.c, SExp())
        # (b . (a . Nil) => (b (a))
        self.b_al = cons(self.b, self.al)
        # ((b . Nil) . (a . Nil)) => ((b) (a))
        self.bl_al = cons(self.bl, self.al)
        # ((b . (a . Nil)) . (c . Nil))
        self.b_al__c = cons(self.b_al, self.cl)
        # (d . ((b . (a . Nil)) . (c . Nil)))
        self.d___b_al__c = cons(self.d, self.b_al__c)

    def testPairStr(self):
        self.assertEqual('()', self.nil.as_pair())
        self.assertEqual('a', self.a.as_pair())
        self.assertEqual('(a . ())', self.al.as_pair())
        self.assertEqual('(b . (a . ()))', self.b_al.as_pair())
        self.assertEqual('((b . ()) . (a . ()))', self.bl_al.as_pair())
        self.assertEqual('((b . (a . ())) . (c . ()))', self.b_al__c.as_pair())
        self.assertEqual('(d . ((b . (a . ())) . (c . ())))', self.d___b_al__c.as_pair())

    def testListStr(self):
        self.assertEqual('()', self.nil.as_list())
        self.assertEqual('a', self.a.as_list())
        self.assertEqual('(a)', self.al.as_list())
        self.assertEqual('(b a)', self.b_al.as_list())
        self.assertEqual('((b) a)', self.bl_al.as_list())
        self.assertEqual('((b a) c)', self.b_al__c.as_list())
        self.assertEqual('(d (b a) c)', self.d___b_al__c.as_list())
