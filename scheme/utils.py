

 
def unique_id():
    """
    Use to assign unique id for each atom
    """
    count = [0]
    def incr():
        count[0] += 1
        return count[0]
    return incr

def ordinal(n):
    """
    Returns an ordinal number decorated string (e.g. '2nd')
    @param n  A integer number
    """
    if 4 <= n <= 20 or 24 <= n <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][n % 10 - 1]
    return str(n)+suffix


def html_spanize(s, classname):
    return '<span class=\"%s\">%s</span>' % (classname, s)
