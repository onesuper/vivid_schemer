from vivid_schemer.playbook.book import Book
from vivid_schemer.play import Play

import click
import readline

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode emacs')

_book = Book('the_little_schemer')
_tree = False

import cmd
import logging

FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)d] %(message)s '
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


class Repl(cmd.Cmd):
    prompt = 'play>'
    intro = 'Usage: [a]bort  [n]ext  [s]tack  [t]op  [h]elp'

    def __init__(self, code, tree_mode=False, debug=False):
        cmd.Cmd.__init__(self)

        print('Debug mode is %s' % ('on' if debug else 'off'))
        print('Tree mode is %s' % ('on' if tree_mode else 'off'))

        logging.getLogger().setLevel(
            logging.DEBUG if debug else logging.INFO)

        self._play = Play(tree_mode=tree_mode)
        self._play.parse(code)

    def do_help(self, arg):
        print('[n]ext\tnext step of evaluation')
        print('[a]bort\tabort the current evaluation')
        print('[h]elp\tprint this message')

    def do_abort(self, arg):
        print('goodbye!')
        return True

    def do_next(self, arg):
        try:
            self._play.next()
        except StopIteration:
            print('Value: %s' % self._play.value)
            return True

    def do_top(self, arg):
        self._play.top()

    def do_stack(self, arg):
        self._play.stack()

    do_h = do_help
    do_t = do_top
    do_n = do_next
    do_a = do_abort
    do_s = do_stack
    do_EOF = do_abort


@click.group()
@click.option('--debug/--no-debug', default=False, help='Enable debug mode.')
@click.option('--tree/--no-tree', default=False,
              help='Display the SExpression in tree mode.')
@click.pass_context
def cli(ctx, debug, tree):
    """A REPL for "The Little Schemer" built with love."""
    ctx.obj = {'debug': debug, 'tree': tree}


@cli.command(short_help='list the chapters')
@click.pass_context
def list(ctx):
    """List all the chapters in "The Little Schemer"."""
    for ch in _book.collect():
        click.echo(ch)


@cli.command(short_help='choose a chapter')
@click.argument('name')
@click.pass_context
def chapter(ctx, name):
    """Choose a chapter in "The Little Schemer" to play."""
    with open(_book.collect()[name]) as fd:
        s = ''.join(fd.readlines())
        cmd = Repl(s, ctx.obj['tree'], ctx.obj['debug'])
        cmd.cmdloop()


@cli.command(short_help='enter the playground')
@click.pass_context
@click.option('--code', '-s', prompt='scheme>',
              help='The code to play.')
def playground(ctx, code):
    """Try with any code in playground."""
    cmd = Repl(code, ctx.obj['tree'], ctx.obj['debug'])
    cmd.cmdloop()


if __name__ == "__main__":
    cli()
