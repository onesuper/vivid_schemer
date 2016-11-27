from vivid_schemer.eval import evaluate, Env
from vivid_schemer.builtin import Builtin, cons, consnil
from vivid_schemer.parser import new_symbol
from vivid_schemer.errors import VividSyntaxError

import unittest


def eval_trace(sexp, env=Env()):
    for x, y, z in evaluate(sexp, env=env):
        print('frame>')
        print(x.as_tree())
        print(y)
        print(z)
        print('-' * 20)


class TestEval(unittest.TestCase):
    def testAtom(self):
        atom = new_symbol('2')
        self.assertIsNone(atom.value)
        eval_trace(atom)
        self.assertEqual(2, atom.value)

        atom = new_symbol('2.22')
        self.assertIsNone(atom.value)
        with self.assertRaises(VividSyntaxError) as cm:
            eval_trace(atom)
        self.assertEqual('SyntaxError: Unrecognized string: 2.22', str(cm.exception))

        atom = new_symbol('abc')
        self.assertIsNone(atom.value)
        eval_trace(atom, Env(abc=199))
        self.assertEqual(199, atom.value)

    def testQuote(self):
        quote = cons(new_symbol('quote'), consnil(new_symbol('a')))
        eval_trace(quote)
        self.assertEqual('a', str(quote.value))

        quote = cons(new_symbol('quote'),
                     consnil(
                         cons(new_symbol('a'),
                              cons(new_symbol('b'),
                                   consnil(new_symbol('c'))))))
        eval_trace(quote)
        self.assertEqual('(a b c)', str(quote.value))

    def testDefine(self):
        env = Env()
        define = cons(new_symbol('define'),
                      cons(new_symbol('a'),
                           consnil(new_symbol('122'))))
        eval_trace(define, env)
        self.assertEqual(122, env['a'])
        self.assertIsNone(define.value)

    def testLambda(self):
        body = cons(new_symbol('*'),
                    cons(new_symbol('r'),
                         consnil(new_symbol('r'))))
        param = consnil(new_symbol('r'))
        func = cons(new_symbol('lambda'),
                    cons(param, consnil(body)))
        eval_trace(func)

    def testProcedure(self):
        proc = cons(new_symbol('plus'),
                    cons(new_symbol('3'),
                         consnil(new_symbol('2'))))
        env = Env(plus=Builtin(lambda x, y: x + y))
        eval_trace(proc, env)

    # def testCond(self):
    #     test1 = cons(SAtom('2'), SExp())
    #     test1 = cons(SAtom('#f'), test1)
    #     test2 = cons(SAtom('3'), SExp())
    #     test2 = cons(SAtom('#t'), test2)
    #     cond = cons(test2, SExp())
    #     cond = cons(test1, cond)
    #     cond = cons(SAtom('cond'), cond)
    #     env = Env(['#t', '#f'], [True, False])
    #     for x, y, z in evaluate(cond, env):
    #         print(x, y, z)
    #     self.assertEqual(3, cond.value)
    #     assert 1==2

    def testBegin(self):
        begin = cons(new_symbol('begin'),
                     cons(new_symbol('199'),
                          cons(new_symbol('1'),
                               consnil(new_symbol('0')))))
        eval_trace(begin)
