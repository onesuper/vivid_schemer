
class VividError(Exception):
    code=1
    def __init__(self, message):
        self.message = message

    # print e
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'Error: %s' % self.message


class LexicalError(VividError):
    pass

class ParserError(VividError):
    pass


class EvalError(VividError):
    """runtime error"""
    def __init__(self, msg):
        VividError.__init__(self, 'eval: %s' % (msg))