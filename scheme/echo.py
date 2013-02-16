#=============================================================
# An interupter for The Little Schemer in Python
# Based on Peter Norvig's lispy.py
# By onesuper
#
# The syntaxes and sementics strictly follow The Little Schemer
#==============================================================

# 
# put a '#' in front of print and the world will be quit


import universe as u
import highlighter as h

class Echo(object):

    def __init__(self, speaker, depth):
        self.speaker = speaker
        self.depth = depth

    def ask(self, message):
        message = h.highlight(message)
        u.hole.append([self.depth, self.speaker, message , 0])
        

    def answer(self, message):
        message = h.highlight(message)
        u.hole.append([self.depth, self.speaker, message, 1])

    def say(self, message):
        message = h.highlight(message)
        u.hole.append([self.depth, self.speaker, message, 2])
