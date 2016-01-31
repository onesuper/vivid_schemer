import unittest
from lib.sexp import SExp, SAtom
from lib.builtin import cons, isatom


class TestSExp(unittest.TestCase):
    def setUp(self):
        self.nil = SExp()
        self.assertFalse(isatom(self.nil))
        self.a = SAtom('a')
        self.assertTrue(isatom(self.a))
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
        print self.nil.pairstr()
        print self.a.pairstr()
        print self.al.pairstr()
        print self.b_al.pairstr()
        print self.bl_al.pairstr()
        print self.b_al__c
        print self.d___b_al__c
        self.assertEqual('()', self.nil.pairstr())
        self.assertEqual('a', self.a.pairstr())
        self.assertEqual('(a . ())', self.al.pairstr())
        self.assertEqual('(b . (a . ()))', self.b_al.pairstr())
        self.assertEqual('((b . ()) . (a . ()))', self.bl_al.pairstr())
        self.assertEqual('((b . (a . ())) . (c . ()))', self.b_al__c.pairstr())
        self.assertEqual('(d . ((b . (a . ())) . (c . ())))', self.d___b_al__c.pairstr())

    def testListStr(self):
        print self.nil.liststr()
        print self.a.liststr()
        print self.al.liststr()
        print self.b_al.liststr()
        print self.bl_al.liststr()
        print self.b_al__c.liststr()
        print self.d___b_al__c.liststr()
        self.assertEqual('()', self.nil.liststr())
        self.assertEqual('a', self.a.liststr())
        self.assertEqual('(a)', self.al.liststr())
        self.assertEqual('(b a)', self.b_al.liststr())
        self.assertEqual('((b) a)', self.bl_al.liststr())
        self.assertEqual('((b a) c)', self.b_al__c.liststr())
        self.assertEqual('(d (b a) c)', self.d___b_al__c.liststr())

    def testTree(self):
        print self.nil.treestr()
        print self.a.treestr()
        print self.al.treestr()
        print self.b_al.treestr()
        print self.bl_al.treestr()
        print self.b_al__c.treestr()
        print self.d___b_al__c.treestr()
