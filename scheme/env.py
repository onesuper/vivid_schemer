#=============================================================
# An interupter for The Little Schemer in Python
# Based on Peter Norvig's lispy.py
# By onesuper
#
# The syntaxes and sementics strictly follow The Little Schemer
#==============================================================




from utils import to_string


class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if var in self else self.outer.find(var)
    def getOuterEnv(self):
        envStr = ""
        if self.outer is not None:
            for k in self.keys():
                envStr += ", {0} is {1}".format(k, to_string(self[k]))
        return envStr
    
            
        
