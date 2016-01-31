
class VividError(Exception):
    code = 1

    def __init__(self, message):
        self.message = message

    # print e
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.message


class VividLexicalError(VividError):
    def __init__(self, msg):
        VividError.__init__(self, 'LexicalError: %s' % msg)


class VividSyntaxError(VividError):
    def __init__(self, msg):
        VividError.__init__(self, 'SyntaxError: %s' % msg)


class VividRuntimeError(VividError):
    def __init__(self, msg):
        VividError.__init__(self, 'RuntimeError: %s' % msg)