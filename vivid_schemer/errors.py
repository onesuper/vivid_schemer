class VividError(RuntimeError):
    def __init__(self, msg):
        super(VividError, self).__init__(msg)


class VividLexicalError(VividError):
    def __init__(self, msg):
        VividError.__init__(self, 'LexicalError: %s' % msg)


class VividSyntaxError(VividError):
    def __init__(self, msg):
        VividError.__init__(self, 'SyntaxError: %s' % msg)


class VividRuntimeError(VividError):
    def __init__(self, msg):
        VividError.__init__(self, 'RuntimeError: %s' % msg)
