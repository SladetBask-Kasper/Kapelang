###
### https://en.wikipedia.org/wiki/Lexical_analysis
###

import string
import headers.Types as Types
a = list(string.ascii_lowercase)
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
separators = list(";,.<>|@!?{([])}&%§")
def lexer(txt):
    ###
    ### This function will tokenize the lines given by the filereader from main.
    ###

    tokens = []

    inString  = False
    appender = ""

    for line in txt:
        for word in line.split():
            if inString:
                if "\"" in word:
                    broken = False
                    for ci in range(len(word)):
                        char = word[ci]
                        if char == "\\":
                            if ci == 0: appender+=" "
                            if broken:
                                appender+="\\\\"
                                broken = False
                            else:
                                broken = True
                        elif broken:
                            if char == "n":
                                appender+="\n"
                                broken = False
                            elif char == "#":
                                appender+="\\#"
                                broken = False
                            else:
                                appender+=char
                                broken = False
                        elif char == "\"" and not broken:
                            inString = False
                            tokens.append(appender)
                            appender=""
                            break
                        else:
                            if ci == 0: appender+=" "
                            appender+=char
                else:
                    appender += " "+word
                continue
            #================================
            #  Done With Strings from here.
            # ===============================
            elif word[0] == "§": pass
            elif word[0] == "\"":
                # string.
                inString = True
                appender = "STR:"+word[1:]
                if word[len(word)-1] == "\"":
                    inString = False
                    tokens.append(appender[:-1])
                    appender=""
                continue
            elif word[0] == "#":
                tokens.append("VAR:"+word[1:])
                continue
            elif word[0] in nums:
                # integer.
                tokens.append("INT:"+word)
            elif word == "print":tokens.append("PRINT")
            elif word == "fprint":tokens.append("PRINTF")
            elif word == "=":tokens.append("ASSIGNMENT")
    return tokens
