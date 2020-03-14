###
### https://en.wikipedia.org/wiki/Parsing
###

from headers.templates import includes
from headers.templates import defines
from headers.templates import funcs
from headers.templates import maine
from headers.lexer import alphabet
from headers.lexer import nums

#import headers.auto as Auto

###
### Translates token datatypes into c++ code datatypes.
### If no datatype is found it returns original value.
###
def datatype_translator(datatype = "CAST_INT"):
    # ======= START OF TYPES ======= #
    if datatype == "CAST_BOOL":
        return "bool"
    elif datatype == "CAST_CSTR":
        return "char*"
    elif datatype == "CAST_INT":
        return "int"
    elif datatype == "CAST_STR":
        return "std::string"
    elif datatype == "CAST_L":
        return "long"
    elif datatype == "CAST_F":
        return "float"
    elif datatype == "CAST_D":
        return "double"
    else:
        return datatype
    # ======= END OF TYPES ======= #

def datatype_to_c(data):
    if data[:4] == "STR:":
        return str(f"(std::string) \"{data[4:]}\"")
    elif data[:4] == "INT:":
        return str(f"(int) {data[4:]}")
    elif data[:5] == "LONG:":
        return str(f"(long) {data[5:]}")
    elif data[:5] == "CSTR:":
        return str(f"(char*) \"{data[5:]}\"")
    elif data[:5] == "BOOL:":
        frlse = "false" # True + False = Frlse
        if data[5:] == "TRUE":
            frlse = "true"
        else: frlse = "false"
        return str(f"(bool) {frlse}")
    elif data[:4] == "VAR:":
        return str(f"{data[4:]}")
    elif data[:10] == "FUNC_NAME:":
            return str(f"{data[10:]}()")
    else:
        return data

def parser(tokens):
    global includes
    global defines
    global funcs
    global maine

    x = 0
    where = "inMaine"
    inIf = 0
    while x < len(tokens):
        code = ""
        if tokens[x] == "PRINT":
            word = ""
            if str(tokens[x+1])[:4] == "STR:":
                word = str(tokens[x+1])[4:]
            code += str(f"std::cout << \"{word}\" << std::endl;")
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
                        if let.lower() in alphabet or let in nums:
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

            code += str(f"std::cout << \"{word}\" << std::endl;")
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
            code += str(f"{t} {varName} = {content};")
            x += 2-1
        elif tokens[x] == "ASSIGN_FUNC" :
            where = "inFunc"
            a = 1 # appender
            funcName = "functionName"
            funcType = "void"
            funcArgs = "()"


            funcType = datatype_translator(tokens[x+a])
            a+=1
            if tokens[x+a][:10] == "FUNC_NAME:":
                funcName = tokens[x+a][10:]
                a += 1
            if tokens[x+a] == "ARG_RANGE":
                a += 1
            else:
                print("ERROR: MALFORMED FUNCTION DECLARATION (misplaced ':' operator)")
                exit()
            args = []
            while not tokens[x+a] == "END_ARGS":
                item = tokens[x+a]
                if item[:5] == "CAST_":
                    args.append(datatype_translator(item))
                elif item == "NEXT":
                    args.append(",")
                elif item[:4] == "VAR:":
                    args.append(item[4:])
                a+=1
            if args[-1:] == ",":
                args = args[:-1]
            funcArgs = "("
            for i in args :
                if i == ",":
                    if funcArgs[-1:] == " ":
                        funcArgs = funcArgs[:-1]

                funcArgs+=i+" "
            if funcArgs[-1:] == " ":
                funcArgs = funcArgs[:-1]
            if funcArgs[-1:] == ",":
                funcArgs = funcArgs[:-1]
            funcArgs += ")"
            x += a-1
            code += str(funcType+" "+funcName+funcArgs)
        elif tokens[x] == "START_SCOPE": code+="\n{\n"
        elif tokens[x] == "END_SCOPE"  :
            code+="\n}\n"
            if inIf > 0:
                inIf-=1
            elif where == "inFunc":
                where = "inMaine"
                funcs+=code
                x += 1
                continue
        elif tokens[x][:5] == "BOOL:":
            code += datatype_to_c(tokens[x])+";" # NOTE : THIS ; DOESN'T SOLVE ANYTHING.
                                                 # For now make sure bools that aren't at
                                                 # The end of line are captured by the
                                                 # Token prior.
        elif tokens[x][:10] == "FUNC_NAME:":
            a = 0
            funcName = "functionName"
            funcArgs = "("

            funcName = tokens[x+a][10:]
            a+=1
            if tokens[x+a] == "ARG_RANGE":
                a+=1
                args = []
                while not tokens[x+a] == "END_ARGS":
                    item = tokens[x+a]
                    if item[:5] == "CAST_":
                        args.append(datatype_translator(item))
                    elif item == "NEXT":
                        args.append(",")
                    elif item[:4] == "VAR:":
                        args.append(item[4:])
                    else:
                        args.append(datatype_to_c(item))
                    a+=1
                if args[-1:] == ",":
                    args = args[:-1]
                funcArgs = "("
                for i in args :
                    if i == ",":
                        if funcArgs[-1:] == " ":
                            funcArgs = funcArgs[:-1]

                    funcArgs+=i+" "
                if funcArgs[-1:] == " ":
                    funcArgs = funcArgs[:-1]
                if funcArgs[-1:] == ",":
                    funcArgs = funcArgs[:-1]
                funcArgs += ")"
                x += a-1
                code += str(funcName+funcArgs+";")
            else:
                code += str(funcName+"();")
        elif tokens[x] == "RETURN":
            if len(tokens) >= x+1:
                code += "return "
            else:
                code += "return;"
        elif tokens[x] == "IF" or tokens[x] == "ELIF":
            command = "yeet"
            if tokens[x] == "IF":
                command = "if"
            else :
                command = "else if"
            a = 1
            if tokens[x+a] == "ARG_RANGE":
                a += 1
                operands = []
                while not tokens[x+a] == "END_ARGS":
                    if tokens[x+a][:5] == "COMP:":
                        operands.append(tokens[x+a][5:])
                    elif tokens[x+a][:4] == "APP:":
                        operands.append(tokens[x+a][4:])
                    else:
                        operands.append(datatype_to_c(tokens[x+a]))
                    a+=1
                code += str(f"{command} ({' '.join(operands)})")
                x += a
                inIf += 1
        elif tokens[x] == "ELSE":
            code += "else"
            inIf += 1


        if where == "inMaine" : maine+=code
        if where == "inFunc"  : funcs+=code
        x += 1
    return str(includes+defines+funcs+maine+"}")
