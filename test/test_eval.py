import unittest
from lib.env import Env
from lib.sexp import SAtom, SExp
from lib.eval import evaluate
from lib.builtin import Builtin, cons


class TestEval(unittest.TestCase):

    def testAtom(self):
        atom = SAtom('2')
        self.assertIsNone(atom.value)
        evaluate(atom)
        self.assertEqual(2, atom.value)

        atom = SAtom('2.22')
        self.assertIsNone(atom.value)
        evaluate(atom)
        self.assertEqual(2.22, atom.value)

        atom = SAtom('abc')
        self.assertIsNone(atom.value)
        evaluate(atom, Env(['abc'], [199]))
        self.assertEqual(199, atom.value)

    def testQuote(self):
        al = cons(SAtom('a'), SExp())
        quote = cons(SAtom('quote'), al)
        evaluate(quote)
        self.assertEqual('a', str(quote.value))

        cl = cons(SAtom('c'), SExp())
        bcl = cons(SAtom('b'), cl)
        abcl = cons(SAtom('a'), bcl)
        abcl_l = cons(abcl, SExp())
        quote = cons(SAtom('quote'), abcl_l)
        evaluate(quote)
        self.assertEqual('(a b c)', str(quote.value))

    def testDefine(self):
        env = Env()
        l = cons(SAtom('122'), SExp())
        al = cons(SAtom('a'), l)
        dal = cons(SAtom('define'), al)
        evaluate(dal, env)
        self.assertEqual(122, env['a'])

    def testLambda(self):
        body = cons(SAtom('r'), SExp())
        body = cons(SAtom('r'), body)
        body = cons(SAtom('*'), body)
        param = cons(SAtom('r'), SExp())
        func = cons(body, SExp())
        func = cons(param, func)
        func = cons(SAtom('lambda'), func)
        evaluate(func)

    def testProcedure(self):
        proc = cons(SAtom('2'), SExp())
        proc = cons(SAtom('3'), proc)
        proc = cons(SAtom('plus'), proc)
        env = Env(['plus'], [Builtin(lambda x, y: x + y)])
        evaluate(proc, env)

    def testCond(self):
        test1 = cons(SAtom('2'), SExp())
        test1 = cons(SAtom('#f'), test1)
        test2 = cons(SAtom('3'), SExp())
        test2 = cons(SAtom('#t'), test2)
        cond = cons(test2, SExp())
        cond = cons(test1, cond)
        cond = cons(SAtom('cond'), cond)
        env = Env(['#t', '#f'], [True, False])
        evaluate(cond, env)
        self.assertEqual(3, cond.value)

    def testBegin(self):
        begin = cons(SAtom('2.2'), SExp())
        begin = cons(SAtom('1'), begin)
        begin = cons(SAtom('199'), begin)
        begin = cons(SAtom('begin'), begin)
        evaluate(begin, Env())
        self.assertEqual(2.2, begin.value)
