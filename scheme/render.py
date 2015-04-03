
HTML_SPACE = '&nbsp;'
HTML_NEWLINE = '<br/>'

class Render:

    tab_size = 2

    def __init__(self, sexpr):
        self.sexpr = sexpr

    def to_html(self):
        '''Render the code to html'''
        if self.sexpr is None:
            raise RuntimeError('The content to render is None!')
        return self.__to_html(self.sexpr, 0, False)

    def __to_html(self, sexpr, level=0, no_indent=False):
        space = HTML_SPACE
        newline = HTML_NEWLINE
        html = ''
        indent = space * level * self.tab_size if not no_indent else ''
        if sexpr.isAtom():
            return str(sexpr.value)
        html += "%s<span id='%d'>(" % (indent, sexpr.id)
        for index,x in enumerate(sexpr.children):
            if x.isAtom():
                html += space if index != 0 else ''
                html += str(x.value)
            elif x.isEmptyList():
                html += space + '()'
            else:
                html += newline if index != 0 else ''
                html += self.__to_html(x, level + 1, False if index != 0 else True)
        html +=")</span>"
        return html

    def to_pretty(self):
        '''Pretty print the scheme code'''
        if self.sexpr is None:
            raise RuntimeError('The content to render is None!')
        return self.__to_pretty(self.sexpr)

    def __to_pretty(self, sexpr, level=0, no_indent=False):
        space = ' '
        newline = '\n'
        s = ''
        indent = space * level * self.tab_size if not no_indent else ''
        if sexpr.isAtom():
            return str(sexpr.value)
        s += "%s(" % (indent)
        for index,x in enumerate(sexpr.children):
            if x.isAtom():
                s += space if index != 0 else ''
                s += str(x.value)
            elif x.isEmptyList():
                s += space + '()'
            else:
                s += newline if index != 0 else ''
                s += self.__to_pretty(x, level + 1, False if index != 0 else True)
        s +=")"
        return s

