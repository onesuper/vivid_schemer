
class VividException(Exception):
    code=1
    def __init__(self, message):
        self.message = message

    # print e
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '{0}'.format(self.message)



class LexicalError(VividException):
    pass

class ParserError(VividException):
    pass
