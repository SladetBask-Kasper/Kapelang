###
### https://en.wikipedia.org/wiki/Parsing
###

from headers.templates import includes
from headers.templates import defines
from headers.templates import funcs
from headers.templates import maine
from headers.lexer import a
from headers.lexer import nums

#import headers.auto as Auto

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
        elif tokens[x] == "PRINTF":
            word = ""
            varName = ""
            if str(tokens[x+1])[:4] == "STR:":
                word = str(tokens[x+1])[4:]
            if word.count("#") > 0:
                varName=""
                inVarName = False
                execute = False
                lets = list(word)
                for i in range(len(lets)):
                    let = lets[i]
                    if inVarName:
                        if let.lower() in a or let in nums:
                            varName += let
                        else:
                            execute = True

                        if i == len(lets)-1:
                            execute = True

                        if execute:
                            inVarName = False
                            appender = str(f"\"<<{varName}<<\"")
                            tmp = word.split("#"+varName)
                            word = tmp[0]+appender+tmp[1]
                            varName = ""
                            execute = False
                    else:
                        if (let == "#") and (not lets[i-1] == "\\"):
                            inVarName = True

            maine += str(f"cout << \"{word}\" << endl;")
            x += 1
        elif tokens[x] == "ASSIGNMENT":
            varName = tokens[x-1][4:]
            content = str(tokens[x+1])[4:]
            types = str(tokens[x+1])[:3]
            t = "auto"
            if types == "INT":
                t = "int"
            elif types == "STR":
                t = "std::string"
                content = str(f"\"{content}\"")
            maine += str(f"{t} {varName} = {content};")
            x += 2


        x += 1
    return str(includes+defines+funcs+maine+"}")
