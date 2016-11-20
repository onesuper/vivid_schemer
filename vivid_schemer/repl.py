from __future__ import print_function

from vivid_schemer.parser import Parser
from vivid_schemer.lexer import Lexer
from vivid_schemer.eval import evaluate, globals
from vivid_schemer.errors import VividError

import sys
import cmd
import logging

FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)d] %(message)s '
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def repl(s, tree=False, debug=False):
    print('Debug mode is %s' % ('on' if debug else 'off'))
    print('Tree mode is %s' % ('on' if tree else 'off'))
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    try:
        lexer = Lexer(s)
        parser = Parser(lexer)
        sexp = parser.form_sexp()
        play = Play(sexp, tree=tree)
        play.cmdloop()
        print('Value: %r' % sexp.value)
    except VividError as e:
        print(e)


class Play(cmd.Cmd):
    prompt = 'play>'
    intro = 'Usage: [a]bort  [c]urrent  [n]ext  [p]revious  [h]elp'
    out = sys.stdout
    err = sys.stderr

    def __init__(self, sexp, tree=False):
        cmd.Cmd.__init__(self)
        self._g = evaluate(sexp, globals())
        self._tree_mode = tree
        self._sexp = None
        self._stack = None
        self._envs = None

    def do_help(self, arg):
        print('[n]ext\tnext step of evaluation', file=self.out)
        print('[a]bort\tabort the current evaluation', file=self.out)
        print('[h]elp\tprint this message', file=self.out)

    def do_abort(self, arg):
        print('goodbye!', file=self.out)
        return True

    def do_next(self, arg):
        try:
            self._sexp, self._stack, self._envs = next(self._g)
            self._show(self._sexp)
        except StopIteration:
            return True
        except VividError as e:
            print(e, file=self.err)

    def do_current(self, arg):
        self._show(self._sexp)

    def _show(self, x):
        print('-' * 40, file=self.out)
        if self._tree_mode:
            print(x.as_tree(), file=self.out)
        else:
            print(x.as_lispm(), file=self.out)

    def do_previous(self, arg):
        frames = zip(self._stack, self._envs)
        for s, e in reversed(frames[:-1]):
            self._show(s)
            #print(e, file=self.out)

    do_c = do_current
    do_n = do_next
    do_a = do_abort
    do_h = do_help
    do_p = do_previous
    do_EOF = do_abort


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
