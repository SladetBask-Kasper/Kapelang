###
### https://en.wikipedia.org/wiki/Lexical_analysis
###

import string
import headers.Types as Types
from headers.trashCollector import trashCollector
alphabet = list(string.ascii_lowercase)
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]
separators = list(";,.<>|@!?{([])}&%§")
comparative_operators = ["==", ">=", "<=", "<", ">", "!="]
appendo_opperators = ["||", "&&", "and", "or"]

def lexer(txt):
    ###
    ### This function will tokenize the lines given by the filereader from main.
    ###

    tokens = []

    inString  = False
    inArgs = False
    appender = ""
    header = False
    inWord = False

    for line in txt:
        #if inArgs :
        #    inArgs = False
        #    tokens.append("END_ARGS")
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
            elif inWord:
                if "´" in word :
                    lastCall = ""
                    for char in list(word):
                        if char == "´":
                            inWord = False
                            tokens.append(appender+" "+lastCall)
                            appender=""
                            break
                        else:
                            lastCall+=char
                else :
                    appender += " "+word
            elif word[0] == "\"":
                # string.
                inString = True
                appender = "STR:"+word[1:]
                if word[len(word)-1] == "\"":
                    inString = False
                    tokens.append(appender[:-1])
                    appender=""
                continue
            #================================
            #  Done With Strings from here.
            # ===============================
            elif word[0] == "´":
                inWord = True
                appender = "WORD_FOR_WORD:"+word[1:]
                if word[-1] == "´":
                    inWord = False
                    tokens.append(appender[:-1])
                    appender=""
            elif word[0] == "§":
                tokens.append("FUNC_NAME:"+word[1:])
                continue
            elif word[0] == "#":
                tokens.append("VAR:"+word[1:])
                continue
            elif word[0] in nums:
                # integer.
                tokens.append("INT:"+word)
            elif word == "print":tokens.append("PRINT")
            elif word == "fprint" or word == "printf":tokens.append("PRINTF")
            elif word == "=":tokens.append("ASSIGNMENT")
            elif word == "func":tokens.append("ASSIGN_FUNC")
            elif word == "}":tokens.append("END_SCOPE")
            elif word == "{":
                if inArgs :
                    inArgs = False
                    tokens.append("END_ARGS")
                tokens.append("START_SCOPE")
            elif word == ":":
                tokens.append("ARG_RANGE")
                inArgs = True
            # ========================================================
            # <CASTS>                                                #
            # ========================================================
            elif word == "int": tokens.append("CAST_INT")
            elif word == "string": tokens.append("CAST_STR")
            elif word == "double": tokens.append("CAST_D")
            elif word == "long": tokens.append("CAST_L")
            elif word == "float": tokens.append("CAST_F")
            elif word == "unsigned": tokens.append("CAST_UNSIGNED")
            elif word == "signed": tokens.append("CAST_SIGNED")
            elif word == "cstr": tokens.append("CAST_CSTR")
            elif word == "bool": tokens.append("CAST_BOOL")
            elif word == "void": tokens.append("CAST_VOID")
            elif word == "u8": tokens.append("CAST_U8")#
            elif word == "s8": tokens.append("CAST_S8")
            elif word == "u16": tokens.append("CAST_U16")
            elif word == "s16": tokens.append("CAST_S16")
            elif word == "u32": tokens.append("CAST_U32")
            elif word == "s32": tokens.append("CAST_S32")
            elif word == "u64": tokens.append("CAST_U64")
            elif word == "s64": tokens.append("CAST_S64")
            elif word == "ul64": tokens.append("CAST_UL64")#
            elif word == "l64": tokens.append("CAST_L64")
            elif word == "uf8": tokens.append("CAST_UF8")#
            elif word == "f8": tokens.append("CAST_F8")
            elif word == "uf16": tokens.append("CAST_UF16")
            elif word == "f16": tokens.append("CAST_F16")
            elif word == "uf32": tokens.append("CAST_UF32")
            elif word == "f32": tokens.append("CAST_F32")
            elif word == "uf64": tokens.append("CAST_UF64")
            elif word == "f64": tokens.append("CAST_F64")
            elif word[:5] == "list<": tokens.append("CAST_V:"+str(word[4:]))#
            # ========================================================
            # </CASTS>                                               #
            # ========================================================
            elif word == "global": tokens.append("DEC_GLOBAL")
            elif word == "|": tokens.append("NEXT")
            elif word == "return": tokens.append("RETURN")
            elif word.lower() == "true": tokens.append("BOOL:TRUE")
            elif word.lower() == "false": tokens.append("BOOL:FALSE")
            elif word == "if": tokens.append("IF")
            elif word == "else": tokens.append("ELSE")
            elif word == "elif": tokens.append("ELIF")
            elif word == "while": tokens.append("WHILE")
            elif word in comparative_operators: tokens.append("COMP:"+word)
            elif word in appendo_opperators: tokens.append("APP:"+(word).replace("and", "&&").replace("or", "||"))
            elif word == "import": tokens.append("IMPORT")
            elif word == "include": tokens.append("INCLUDE")
            elif word == "use": tokens.append("USE")
            elif word == "new": tokens.append("ASSIGN_NEW")
            elif word == "!!HEADER_FILE!!" :
                tokens.append("HEADER:__THIS__")
                header = True
            elif word == "define" : tokens.append("DEFINE")
        if inArgs :
            inArgs = False
            tokens.append("END_ARGS")
    if header : return tokens
    else : return trashCollector(tokens)
