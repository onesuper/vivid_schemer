from parser import Parser
from lexer import Lexer
from eval import evaluate
from errors import VividRuntimeError, VividLexicalError, VividSyntaxError
from globals import add_globals
from env import Env


def vivid(s):
    try:
        lexer = Lexer(s)
        parser = Parser(lexer)
        sexp = parser.form_sexp()
    except VividSyntaxError, e:
        print e
        return
    except VividLexicalError, e:
        print e
        return

    root = sexp
    g = evaluate(root, add_globals(Env()))
    sexp, stack, envs = g.next()
    # print sexp.treestr(),
    print sexp.liststr_l()

    while True:
        line = raw_input('vivid>')
        arr = line.split()
        if len(arr) > 1:
            cmd, argv = arr[0], arr[1:]
        else:
            cmd, argv = line, []
        if cmd == 'e' or cmd == 'env':
            if len(argv) > 0:
                if argv[0] in envs[-1]:
                    print envs[-1][argv[0]]
            else:
                print envs[-1]
        elif cmd == 'n' or cmd == 'next':
            try:
                sexp, stack, envs = g.next()
                # print sexp.treestr(),
                print sexp.liststr_l()

            except StopIteration:
                print 'over'
                break
            except VividRuntimeError, e:
                print e
                break
        elif cmd == 'l' or cmd == 'list':
            print sexp.liststr_l()
        elif cmd == 't' or cmd == 'tree':
            if len(argv) > 0:
                t = root.find(int(argv[0]))
                if t is not None:
                    print t.treestr()
            else:
                print sexp.treestr()
        elif cmd == 'r' or cmd == 'root':
            print root.treestr()
        elif cmd == 'f' or cmd == 'fold':
            if len(argv) > 0:
                t = root.find(int(argv[0]))
                if t is not None:
                    if t.folded:
                        t.unfold()
                    else:
                        t.fold()
        elif cmd == 'a' or cmd == 'abort':
            break
        elif cmd == 'h' or cmd == 'help':
            usage()
        elif cmd == 'l' or cmd == 'law':
            if len(argv) > 0:
                proc = argv[0]
                if proc in envs[-1]:
                    law(envs[-1][proc].name, envs[-1][proc].law)
        elif cmd == 'q' or cmd == 'quit':
            import sys
            sys.exit(0)
        elif cmd == 'd' or cmd == 'debug':
            print stack
            print envs
        else:
            print 'unkown command'


def usage():

    prompt_line()

    print '''abort\tabort the current evaluation
next\tnext step of evaluation
env\tshow everything in the environment
list\tdisplay the S-expression as a list
tree\tdisplay the S-expression as a tree
root\tdisplay the S-expression  from the root
fold\tfold or unfold a S-expression node
help\tprint this message
law\tshow the law of a primitive
quit\tgoodbye
'''


def prompt_line():
    print 'Usage: [a]bort  [n]ext  [e]nv  [l]ist  [t]ree  [r]oot  [f]old  [l]aw   [h]elp  [q]uit'


def law(name, content):
    line = '=' * 64
    print line
    print "{:^64}".format("The Law of " + str(name).capitalize())
    text = []
    while True:
        if len(content) < 60:
            text.append(content)
            break
        text.append(content[:60])
        content = content[60:]
    for t in text:
        print "  " + "{:<60}".format(t)
    print line

