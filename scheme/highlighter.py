# highlighting a message


def p(match):
    return '<span class="p">' + match.group(0) + '</span>'

def number(match):
    return '<span class="number">' + match.group(0) + '</span>'

def keyword(match):
    return '<span class="keyword">' + match.group(0) + '</span>'

def boolean(match):
    return '<span class="boolean">' + match.group(0) + '</span>'

KEYWORD = r'\bdefine\b|\bbegin\b|\blambda\b|\bquote\b|\bcond\b|\bor\b|\band\b|\belse\b|\beq\?\b|\batom\?\b|\bnull\?\b|\bzero\?\b|\bcar\b|\bcdr\b|\bcons\b|\bif\b|\bmap\b'


import re

def highlight(message):
    message = re.sub(KEYWORD, keyword, message)
    message = re.sub(r'\(|\)', p, message)
    message = re.sub(r'\d+', number, message)
    message = re.sub(r'#f|#t', boolean, message)
    return message

