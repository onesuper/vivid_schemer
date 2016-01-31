class Env(dict):
    def __init__(self, parms=(), args=()):
        dict.__init__(self)
        self.update(zip(parms, args))

    def __repr__(self):
        return '{' + ','.join(self.keys()) + '}'
