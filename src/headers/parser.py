###
### https://en.wikipedia.org/wiki/Parsing
###

from headers.templates import includes
from headers.templates import defines
from headers.templates import funcs
from headers.templates import maine

def parser(tokens):
    global includes
    global defines
    global funcs
    global maine
    x = 0
    while x < len(tokens):
        if tokens[x] == "PRINT":
            word = ""
            if str(tokens[x+1])[:4] == "STR:":
                word = str(tokens[x+1])[4:]
            maine += str(f"cout << \"{word}\" << endl;")
            x += 1
        x += 1
    return str(includes+defines+funcs+maine+"}")
