import logging
from clint.textui import colored

LOG = logging.getLogger(__name__)


class SExp(object):
    """S-expression representaion of AST like (x . (y . z)) rather then list"""
    __sid = 0

    @staticmethod
    def get_id():
        old = SExp.__sid
        SExp.__sid += 1
        return old

    def __init__(self):
        """Construct an empty list expression (a.k.a Nil)"""
        self._id = SExp.get_id()
        self._car = None
        self._cdr = None
        self._value = None
        self._msg = None
        self._is_show_value = False
        self._is_folded = False
        self._is_list_view = True
        self._is_visited = False  # for tree walk

    @property
    def id(self):
        return self._id

    @property
    def car(self):
        return self._car

    @property
    def cdr(self):
        return self._cdr

    @property
    def value(self):
        return self._value

    @property
    def msg(self):
        return self._msg

    @property
    def is_visited(self):
        return self._is_visited

    def set_msg(self, value, color='white'):
        LOG.debug('set [%s] msg: %s' % (self._id, value))
        if color == 'red':
            self._msg = colored.red(value)
        elif color == 'green':
            self._msg = colored.green(value)
        else:
            self._msg = value

    def assign_value(self, value):
        LOG.debug('assign [%s] value: %s' % (self._id, value))
        self._value = value

    def mark_visited(self):
        LOG.debug('mark [%s] visited' % self._id)
        self._is_visited = True

    def __str__(self):
        return SExp._shorthand(self.as_list() if self._is_list_view else self.as_pair())

    def __repr__(self):
        return self.as_list()

    # def __len__(self):
    #     return len(self.to_list())

    def to_list(self):
        """Flatten an S-expression to a list representation
        e.g (x y z) => [x, y, z]"""
        l = []
        x = self
        while True:
            if x.isnil():
                break
            l.append(x._car)
            x = x._cdr
        return l

    def find(self, id):
        if self._id == id:
            return self
        else:
            if self._car:
                x = self._car.find(id)
                if x is None:
                    if self._cdr:
                        x = self._cdr.find(id)
                    return x
                else:
                    return x

    def fold(self):
        self._is_folded = True

    def unfold(self):
        self._is_folded = False

    def fold_all(self):
        if self.isnil():
            return
        self.fold()
        self._car.fold_all()
        self._cdr.fold_all()

    def unfold_all(self):
        if self.isnil():
            return
        self.unfold()
        self._car.unfold_all()
        self._cdr.unfold_all()

    def isnil(self):
        """Whether it is a Nil node"""
        return self._car is None and self._car is None

    def as_pair(self):
        """The original structure for S-expressions e.g. (x . (y . (z . () )))"""
        items = []
        if self.isnil():
            return '()'
        if self._car:
            items.append(self._car.as_pair())
            items.append('.')
        if self._cdr:
            items.append(self._cdr.as_pair())
        s = '(' + ' '.join(items) + ')'
        return s

    def as_list(self, flatten=False):
        """Render as Lisp-readable string e.g. (x y z)"""
        if self.isnil():
            return '()'
        items = []
        if self._car:
            items.append(self._car.as_list(False))
        if self._cdr:
            if not self._cdr.isnil():
                # flatten the cdr chain
                s = self._cdr.as_list(True)
                items.append(s)
        if flatten:
            return ' '.join(items)
        else:
            return SExp._join_paren(items)

    def as_pretty_list(self, flatten=False, indent='  ', newline='\n', depth=0):
        """Multi-line lisp-readable string containing message above each (cdr)"""
        if self.isnil():
            return '()'
        items = []
        if self._car:
            items.append(self._car.as_pretty_list(False, indent, newline, depth + 1))
        if self._cdr:
            if not self._cdr.isnil():
                # flatten the cdr chain
                s = self._cdr.as_pretty_list(True, indent, newline, depth)
                items.append(s)
        if flatten:
            return ' '.join(items)
        else:
            line = newline
            if self._msg:
                line += indent * depth + str(self._msg) + newline
            line += indent * depth + SExp._join_paren(items)
            return line

    @classmethod
    def _join_paren(cls, items):
        return '(' + ' '.join(items) + ')'

    def as_tree(self, indent='  ', newline='\n', depth=0):
        """Recursively echo the AST tree based on the S-expresssion.
        The leaves are indented according to their depth on the tree.
        Each leave can be previewed as a pair or a list string."""
        s = indent * depth
        s += '|%s' % ('+' if self._is_folded else '-')
        s += 'S%d: ' % self._id
        if self._is_folded:
            s += '\'%s\'' % SExp._shorthand(self.as_list() if self._is_list_view else self.as_pair())
        if self._msg:
            s += ' %s' % self._msg
        if self._is_show_value:
            s += ' (%s)' % repr(self._value)
        s += newline
        if self._is_folded:  # do not show child
            return s
        if self._car:
            s += self._car.as_tree(indent, newline, depth + 1)
        if self._cdr:
            s += self._cdr.as_tree(indent, newline, depth + 1)
        return s

    @classmethod
    def _shorthand(cls, s):
        if len(s) > 50:
            return s[:50] + '...'
        else:
            return s


class SAtom(SExp):
    def __init__(self, literal):
        super(SAtom, self).__init__()
        assert isinstance(literal, str)
        self._literal = literal

    def isnil(self):
        return False

    def as_pair(self):
        return self._literal

    def as_list(self, flatten=False):
        return self._literal

    def as_pretty_list(self, flatten=False, indent='  ', newline='\n', depth=0):
        s = self._literal
        return s

    def as_tree(self, indent='  ', newline='\n', depth=0, lisp=False):
        s = indent * depth
        s += '|-S%d: ' % self._id
        s += '\'%s\'' % (self.as_list() if lisp else self.as_pair())
        if self._msg:
            s += ' %s' % self._msg
        if self._is_show_value:
            s += ' (%s)' % repr(self._value)
        s += newline
        return s

    def __str__(self):
        return self._literal

    def __repr__(self):
        return self._literal

    def startswith_nondigit(self):
        import re
        return re.match(r'^[^0-9].*$', self._literal)

    def isdigits(self):
        import re
        return re.match(r'^\d+$', self._literal)

    def fold(self):
        pass

    def unfold(self):
        pass

    def fold_all(self):
        pass

    def unfold_all(self):
        pass
