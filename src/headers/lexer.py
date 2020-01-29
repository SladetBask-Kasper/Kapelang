###
### https://en.wikipedia.org/wiki/Lexical_analysis
###

import string
import headers.Types as Types
a = list(string.ascii_lowercase)
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def lexer(txt):
    ###
    ### This function will tokenize the lines given by the filereader from main.
    ###

    tokens = []

    inComment = False
    inString  = False
    inInt     = False
    inFunc    = False
    for line in txt:
        command = ""
        commandType = Types.null
        for char in list(line):
            if char == "\"":
                inString = not inString
                if not inString:
                    tokens.append("STR:"+command)
                continue
            if inString or inInt:
                command += char
            elif command == "fprint":
                tokens.append("PRINTF")
                command = ""
            elif command == "print":
                tokens.append("PRINT")
                command = ""
            elif char in nums:
                try:
                    tmp = int(command.strip())
                except:
                    pass
                command = command.strip()+char
                inInt = True
            elif char.lower() in a:
                command += char
            elif char == '.':
                commandType = Types.classes
                command += char
            elif char == "#":
                if command.strip()=="int":
                    tokens.append("VAR_INT")
                if command.strip()=="str":
                    tokens.append("VAR_STR")
            elif char == "§":
                commandType = Types.function
            elif char == "=":
                tokens.append("ASSIGNMENT")
                tokens.append(command)
                command = ""
        if commandType == Types.function:
            tokens.append("FUNC_NAME:"+command)
        if inInt:
            tokens.append("INT:"+command)
            inInt = False
    return tokens
