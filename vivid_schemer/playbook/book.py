import os
from pkg_resources import resource_filename


class Book(object):
    """Manages the book in the form of files on the disk"""
    def __init__(self, name):
        self._chapters = Book._collect_chapters(name)

    @staticmethod
    def _collect_chapters(book_name):
        chapters = {}
        book_dir = _abspath(resource_filename(__name__, book_name))
        for root, dirs, files in os.walk(book_dir):
            for f in files:
                fname = str(f)
                if fname.endswith('.scm'):
                    chapters[f] = os.path.join(root, f)
        return chapters

    def collect(self):
        return self._chapters


def _cleanpath(*args):
    parts = [args[0].strip()]
    for arg in args[1:]:
        parts.append(
            (arg.replace(os.path.sep, '', 1) if arg.startswith(os.path.sep) else arg).strip())
    return parts


def _abspath(*args):
    return os.path.realpath(
        os.path.expanduser(
            os.path.join(
                *_cleanpath(*args))))
