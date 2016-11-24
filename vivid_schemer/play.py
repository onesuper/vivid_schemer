from __future__ import print_function

from vivid_schemer.parser import Parser
from vivid_schemer.lexer import Lexer
from vivid_schemer.eval import evaluate, globals

import sys


class Play(object):
    def __init__(self, out=sys.stdout, err=sys.stderr):
        self._gen = None
        self._sexp = None
        self._stack = None
        self._envs = None
        self._out, self._err = out, err

    def parse(self, s):
        lexer = Lexer(s)
        parser = Parser(lexer)
        self._sexp = parser.form_sexp()
        self._gen = evaluate(self._sexp, globals())

    def next(self):
        self._sexp, self._stack, self._envs = next(self._gen)
        self._show(self._sexp)

    def stack(self, mode='pretty'):
        frames = zip(self._stack, self._envs)
        for s, e in reversed(frames[:-1]):
            self._show(s, mode)

    def top(self, mode='pretty'):
        self._show(self._sexp, mode)

    def _show(self, x, mode):
        print('-' * 40, file=self._out)
        if mode == 'tree':
            print(x.as_tree(), file=self._out)
        elif mode == 'pair':
            print(x.as_pair(), file=self._out)
        elif mode == 'list':
            print(x.as_list(), file=self._out)
        else:
            print(x.as_pretty_list(), file=self._out)

    def __iter__(self):
        return self

    def __next__(self):
        self.next()
        return self

    @property
    def value(self):
        return self._sexp.value


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
