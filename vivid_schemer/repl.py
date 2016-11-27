from __future__ import print_function

from vivid_schemer.parser import Parser
from vivid_schemer.lexer import Lexer
from vivid_schemer.eval import evaluate, Env
from vivid_schemer.builtin import *

import sys

_global_envs = {
    'cdr': Builtin(cdr),
    'car': Builtin(car),
    'cons': Builtin(cons),
    'atom?': Builtin(isatom, 'Is it true that this is an atom? %r'),
    'list?': Builtin(islist, 'Is it true that this is a list? %r'),
    'sexp?': Builtin(issexp, 'Is it true that this is an S-expression? %r'),
    'null?': Builtin(isnull, 'null?'),
    'eq?': Builtin(iseq, 'eq?'),
    'add1': Builtin(lambda x: x + 1, 'add1'),
    'sub1': Builtin(lambda x: x - 1, 'sub1'),
    'how-many-sexps?': Builtin(how_many_sexps,
                               'How many S-expressions are in the list %r and what are they?'),
    # 'equal?':   is_equal,
    # 'zero?':    is_zero,
    # 'member?':  is_member,
    # 'number?':  is_number,
    # 'map':      map_,

    # arithmetic
    '+': Builtin(lambda x, y: x + y, 'add'),
    '-': Builtin(lambda x, y: x - y, 'sub'),
    '*': Builtin(lambda x, y: x * y, 'mult'),
    '/': Builtin(lambda x, y: x / y, 'div'),
    '>': Builtin(lambda x, y: x > y, 'gt'),
    '<': Builtin(lambda x, y: x < y, 'lt'),
    '>=': Builtin(lambda x, y: x >= y, 'gte'),
    '<=': Builtin(lambda x, y: x <= y, 'lte'),
    '=': Builtin(lambda x, y: x == y, 'eq'),
    '^': Builtin(lambda x, y: x ** y, 'power'),
    'not': Builtin(lambda x: ~x, 'not'),

    # var
    '#t': True,
    '#f': False,
    'else': True,
}


class Repl(object):
    def __init__(self, out=sys.stdout, err=sys.stderr):
        self._gen = None
        self._stack = None
        self._envs = None
        self._out, self._err = out, err
        self._end_loop = True

    def read(self, s):
        lexer = Lexer(s)
        parser = Parser(lexer)
        self._envs = [Env(**_global_envs)]
        self._stack = [parser.form_sexp()]
        self._gen = evaluate(self._stack, self._envs)
        self._end_loop = False

    def eval(self):
        if self._end_loop:
            raise StopIteration
        try:
            tos, self._stack, self._envs = next(self._gen)
            return tos.value
        except StopIteration:
            self._end_loop = True

    def stack(self, mode='pretty'):
        frames = list(zip(self._stack, self._envs))
        for s, e in reversed(frames):
            print('-' * 40, file=self._out)
            self._show(s, mode)

    def top(self, mode='pretty'):
        self._show(self._stack[-1], mode)

    def _show(self, x, mode):
        if mode == 'tree':
            print(x.as_tree().strip(), file=self._out)
        elif mode == 'pair':
            print(x.as_pair(), file=self._out)
        elif mode == 'list':
            print(x.as_list(), file=self._out)
        else:
            print(x.as_pretty_list().strip(), file=self._out)

    def __iter__(self):
        return self

    def __next__(self):
        self.eval()
        return self


def exlude_globals(envs):
    global_keys = globals().keys()
    new_envs = []
    for env in envs:
        new_env = {}
        for k, v in env.items():
            if k not in global_keys:
                new_env[k] = v
        new_envs.append(new_env)
    return new_envs


def print_law(name, content):
    separator = '=' * 64
    print(separator)
    print("{:^64}".format("The Law of " + str(name).capitalize()))
    text = []
    while True:
        if len(content) < 60:
            text.append(content)
            break
        text.append(content[:60])
        content = content[60:]
    for t in text:
        print("  " + "{:<60}".format(t))
    print(separator)
