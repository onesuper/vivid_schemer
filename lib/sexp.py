

class SExp:
    """S-expression representaion of AST like (x . (y . z)) rather then list"""
    sid = 0
    folded = False

    @staticmethod
    def get_id():
        old = SExp.sid
        SExp.sid += 1
        return old

    def __init__(self):
        """Construct an empty list expression (a.k.a Nil)"""
        self.id = SExp.get_id()
        self.car = None
        self.cdr = None
        self.value = None
        self.msg = None
        self.show_value = False
        self.folded = SExp.folded
        self.lisp_view = True
        self.visited = False   # for tree walk

    def __str__(self):
        return shorthand(self.liststr() if self.lisp_view else self.pairstr())

    def __repr__(self):
        s = '<@SExp[%d]: ' % self.id
        s += '\'%s\'>' % str(self)
        return s

    def find(self, _id):
        if self.id == _id:
            return self
        else:
            if self.car:
                x = self.car.find(_id)
                if x is None:
                    if self.cdr:
                        x = self.cdr.find(_id)
                    return x
                else:
                    return x

    def fold(self):
        self.folded = True

    def unfold(self):
        self.folded = False

    def fold_all(self):
        if self.isnil():
            return
        self.fold()
        self.car.fold_all()
        self.cdr.fold_all()

    def unfold_all(self):
        if self.isnil():
            return
        self.unfold()
        self.car.unfold_all()
        self.cdr.unfold_all()

    def isnil(self):
        """Whether it is a Nil node"""
        return self.car is None and self.car is None

    def pairstr(self):
        """The orginal structure for S-expressions e.g. (x . (y . (z . () )))"""
        items = []
        if self.isnil():
            return '()'
        if self.car:
            items.append(self.car.pairstr())
            items.append('.')
        if self.cdr:
            items.append(self.cdr.pairstr())
        s = '(' + ' '.join(items) + ')'
        return s

    def liststr(self, flatten=False):
        """Render as Lisp-readable string e.g. (x y z)"""
        if self.isnil():
            return '()'
        items = []
        if self.car:
            items.append(self.car.liststr(False))
        if self.cdr:
            if not self.cdr.isnil():
                s = self.cdr.liststr(True)  # flatten the cdr chain
                items.append(s)
        if flatten:
            return ' '.join(items)
        else:
            return '(' + ' '.join(items) + ')'

    def liststr_l(self, flatten=False, indent='  ', newline='\n', depth=0):
        """Multi-line lisp-readable string"""
        if self.isnil():
            return '()'
        items = []
        if self.car:
            items.append(self.car.liststr_l(False, indent, newline, depth+1))
        if self.cdr:
            if not self.cdr.isnil():
                s = self.cdr.liststr_l(True, indent, newline, depth)  # flatten the cdr chain
                items.append(s)
        if flatten:
            return ' '.join(items)
        else:
            line = newline
            if self.msg:
                line += indent * depth + '%s\n' % self.msg
            line += indent * depth + '(' + ' '.join(items) + ')'
            return line

    def treestr(self, indent='  ', newline='\n', depth=0):
        """Recursively echo the AST tree based on the S-expresssion.
        The leaves are indented according to their depth on the tree.
        Each leave can be previewed as a pair or a list string."""
        s = indent * depth
        s += '`%s' % ('+' if self.folded else '-')
        s += 'SExp[%d]: ' % self.id
        if self.folded:
            s += '\'%s\'' % shorthand(self.liststr() if self.lisp_view else self.pairstr())
        if self.msg:
            s += ' %s' % self.msg
        if self.show_value:
            s += ' (%s)' % repr(self.value)
        s += newline
        if self.folded:  # do not show child
            return s
        if self.car:
            s += self.car.treestr(indent, newline, depth+1)
        if self.cdr:
            s += self.cdr.treestr(indent, newline, depth+1)
        return s


def shorthand(s):
    if len(s) > 50:
        return s[:50] + '...'
    else:
        return s


class SAtom(SExp):
    def __init__(self, literal):
        SExp.__init__(self)
        assert isinstance(literal, str)
        self.literal = literal

    def isnil(self):
        return False

    def pairstr(self):
        return self.literal

    def liststr(self, flatten=False):
        return self.literal

    def liststr_l(self, flatten=False, indent='  ', newline='\n', depth=0):
        s = self.literal
        return s

    def treestr(self, indent='  ', newline='\n', depth=0, lisp=False):
        s = indent * depth
        s += '`-SAtom[%d]: ' % self.id
        s += '\'%s\'' % (self.liststr() if lisp else self.pairstr())
        if self.msg:
            s += ' %s' % self.msg
        if self.show_value:
            s += ' (%s)' % repr(self.value)
        s += newline
        return s

    def __str__(self):
        return self.literal

    def fold(self):
        pass

    def unfold(self):
        pass

    def fold_all(self):
        pass

    def unfold_all(self):
        pass
