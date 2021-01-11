###
### https://en.wikipedia.org/wiki/Parsing
###

from headers.templates import includes
from headers.templates import defines
from headers.templates import funcs
from headers.templates import maine
from headers.templates import packages
from headers.templates import globals
from headers.lexer import alphabet
from headers.lexer import nums
from headers.toolbox import *

def e(x):
    idk = 0
    instance = 0
    idk += 1
    print(f"[i{instance}, p{idk}] - {x}")

#import headers.auto as Auto # old toolbox

def parser(tokens):
    global includes
    global defines
    global funcs
    global maine
    global globals

    x = 0
    where = "inMaine"
    inIf = 0
    isHeader = False
    useKabeTypes = True

    while x < len(tokens):
        code = ""
        if tokens[x] == "PRINT":
            code += str(f"std::cout << {trans(tokens[x+1])} << std::endl;")
            x += 1
        elif tokens[x] == "PRINTF":
            #print("Entered printf")
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
            t = "auto"
            if str(tokens[x+1])[:5] == "CAST_":
                t = datatype_translator(tokens[x+1])
                newContent = tokens[x+2]
                a = 0
                if (len(newContent) >= 5 and newContent[:5] == "FUNC_"):
                    newContent = tokens[x+2][10:]
                    a = 3
                    arguments = "("
                    if tokens[x+a] == "ARG_RANGE":
                        a+=1
                        while not tokens[x+a] == 'END_ARGS':
                            if tokens[x+a] == "NEXT":
                                pass
                            else:
                                arguments += datatype_to_c(tokens[x+a]) + ", "
                            a+=1
                        arguments = arguments[:-2]
                    arguments += ")"
                    newContent += arguments
                else:
                    newContent = newContent[4:]
                content = str(f"({t}) {newContent}")
                x+=a-2 #when this was at -1 I had a problem in the file hasher example with print.
            else:
                types = str(tokens[x+1])[:3]
                if types == "INT":
                    t = "int"
                elif types == "STR":
                    t = "std::string"
                    content = str(f"\"{content}\"")
                elif types == "FUN":
                    t = str(tokens[x+1])[10:]
                    argl = ""
                    if tokens[x+2] == "ARG_RANGE":
                        more = True
                        count = 0
                        while more:
                            count += 1
                            index = count + (x+2)
                            if tokens[index] == "NEXT":
                                continue
                            elif tokens[index] == "END_ARGS":
                                more = False
                                break
                            else:
                                argl += datatype_to_c(tokens[index])+", "
                    argl = argl.strip()
                    if len(argl) > 0 and (argl[-1] == ","):
                        argl = argl[:-1]
                    content = t + f"({argl})"

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
                elif len(item) >= 10 and item[:10] == "FUNC_NAME:":
                    # if so it's a class
                    args.append(item[10:])
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
            code += datatype_to_c(tokens[x])+";" # NOTE : THIS DOESN'T SOLVE ANYTHING.
                                                 # For now make sure bools that aren't at
                                                 # The end of line are captured by the
                                                 # Token prior.
        elif tokens[x][:10] == "FUNC_NAME:":
            a = 0
            funcName = "functionName"
            funcArgs = "("

            funcName = tokens[x+a][10:]
            a+=1
            if len(tokens) <= x+2:
                a=0
            if tokens[x+a] == "ARG_RANGE":
                a+=1
                args = []
                while not tokens[x+a] == "END_ARGS":
                    if tokens[x+a] == "END_ARGS":
                        break
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
                    a-=1
                funcArgs = "("
                for i in args :
                    if i == ",":
                        if funcArgs[-1:] == " ":
                            funcArgs = funcArgs[:-1]
                            a-=1
                    funcArgs+=i+" "
                if funcArgs[-1:] == " ":
                    funcArgs = funcArgs[:-1]
                    a-=1
                if funcArgs[-1:] == ",":
                    funcArgs = funcArgs[:-1]
                    a-=1
                funcArgs += ")"
                #x += a-1 # minus should be applied at appropriate place
                x += a
                code += str(funcName+funcArgs+";")
            else:
                code += str(funcName+"();")
        elif tokens[x] == "RETURN":
            if len(tokens) >= x+1:
                if tokens[x+1][:4] == "VAR:":
                    code += str(f"return {tokens[x+1][4:]};")
                elif tokens[x+1] == "END_SCOPE":
                    code += "return;"
                else : code += "return "
            else:
                code += "return;"
        elif tokens[x] == "IF" or tokens[x] == "ELIF":
            command = "yeet"
            if tokens[x] == "WHILE":
                command = "while"
            elif tokens[x] == "IF":
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
        elif tokens[x] == "DEC_GLOBAL":
            type = datatype_translator(tokens[x+1])
            name = datatype_to_c(tokens[x+2])
            assignmentType = tokens[x+3]
            #dataType = str(tokens[x+4])[:3]
            data = datatype_to_c(tokens[x+4])
            globals += f"{type} {name} = {data};\n"
            x+=4

        elif tokens[x] == "USE":
            x+=1
            toUse = tokens[x][4:]
            defines+= f"using {toUse};"
        elif tokens[x] == "IMPORT":
            if len(tokens) >= x+1:
                x+=1
                includes += str(f"#include <{tokens[x][4:]}>\n") # 4: because we expect a string.
        elif tokens[x] == "INCLUDE":
            if len(tokens) >= x+1:
                x+=1
                includes += str(f'#include "{packages+(tokens[x][4:])}.h"\n')
        elif tokens[x] == "HEADER:__THIS__":
            isHeader = True
        elif tokens[x] == "DEFINE":
            if tokens[x+1][:14] == "WORD_FOR_WORD:":
                defines+="#define "+tokens[x+1][14:]+"\n"
                x+=1
        elif tokens[x][:5] == "CAST_":
            code += str(f"({datatype_translator(tokens[x])})")
        elif tokens[x][:14] == "WORD_FOR_WORD:":
            code += tokens[x][14:]



        if where == "inMaine" : maine+=code
        if where == "inFunc"  : funcs+=code
        x += 1
    if isHeader:
        includes = "#pragma once\n"+includes
    if useKabeTypes:
        includes += str(f'#include "{packages}stdkabe.h"\n')
    returnValue = str(includes+defines+globals+funcs)
    if not isHeader:
        returnValue+=maine+"return 0;}"
    return returnValue#.replace(";", ";\n") # Uncomment to make code slightly more readable.
