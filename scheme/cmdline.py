


class Echo(object):
    """
    Dump everything to command line.
    This class is used to test on the back end.
    """

    indent = '\t'

    def __init__(self, speaker, depth):
        """
        @param speaker A string specifying who ask and answer question
        @param depth   Recursion depth
        """
        self.speaker = speaker
        self.depth = depth

    def _talk(self, msg):
        print "%s%s: %s" % (self.depth * self.indent, self.speaker, msg)

    def ask(self, msg):
        self._talk(msg)
        
    def answer(self, msg):
        self._talk(msg)

    def say(self, msg):
        self._talk(msg)
