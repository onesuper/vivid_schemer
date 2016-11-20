from vivid_schemer.playbook.book import Book
from vivid_schemer.repl import repl

import click
import readline

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode emacs')

_book = Book('the_little_schemer')
_tree = False


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
        repl(s, ctx.obj['tree'], ctx.obj['debug'])


@cli.command(short_help='enter the playground')
@click.pass_context
@click.option('--code', '-s', prompt='scheme>',
              help='The code to play.')
def playground(ctx, code):
    """Try with any code in playground."""
    repl(code, ctx.obj['tree'], ctx.obj['debug'])


if __name__ == "__main__":
    cli()
