

from universe import hole
from lexer import Lexer

def par(match):
    return html_spanize(match.group(0), 'p')

def number(match):
    return html_spanize(match.group(0), 'number')

def keyword(match):
    return html_spanize(match.group(0), 'keyword')

def boolean(match):
    return html_spanize(match.group(0), 'boolean')

def highlight(message):
    """
    Fetch the rule from `Lexer` and do string substitution 
    """
    import re
    message = re.sub(Lexer.KEYWORD, keyword, message)
    message = re.sub(Lexer.PAR, par, message)
    message = re.sub(Lexer.INTEGER, number, message)
    message = re.sub(Lexer.BOOL, boolean, message)
    return message

class Echo(object):
    """
    Dump everything to a hole in the universe to communicate with
    the front end.
    """
    
    def __init__(self, speaker, depth):
        """
        @param speaker A string specifying who ask and answer question
        @param depth   The recursion depth
        """
        self.speaker = speaker
        self.depth = depth

    def _talk(self, msg, kind):
        msg = highlight(msg)
        hole.append([self.depth, self.speaker, msg , kind])

    def ask(self, msg):
        self._talk(msg, 0)
        
    def answer(self, msg):
        self._talk(msg, 1)


    def say(self, msg):
        self._talk(msg, 2)

