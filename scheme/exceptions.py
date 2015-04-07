
class VividException(Exception):
    code=1
    def __init__(self, message):
        self.message = message

    # print e
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '%s' % self.message


class LexicalError(VividException):
    pass

class ParserError(VividException):
    pass


class SyntaxError(VividException):
    def __init__(self, msg, lineno, colno):
        VividException.__init__(self, 'line: %d, col: %d: %s' % (lineno, colno, msg))

class WrongParamsError(SyntaxError):
    def __init__(self, name, numParams, lineno, colno):
        VividException.__init__(self, SyntaxError('%s should have %d parameters' %
            (name, numParams), lineno, colno))
