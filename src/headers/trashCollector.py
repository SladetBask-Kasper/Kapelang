tokens = []
idk = 0
instance = 0

def e(x):
    global idk
    global instance
    idk += 1
    print(f"[i{instance}, p{idk}] - {x}")

def clean(start, finish):
    global tokens
    while start <= finish:
        del tokens[finish]
        finish -= 1 # we need to go backwards so that the indexes don't move.
    return

def trashCollector(data, recur = 1):
    global instance
    if len(data)<5:
        return data# too small program to bother running in to uneccessary errors.
    global tokens

    tokens = data
    del data
    x = 0
    while x < len(tokens):
        if x < 0:
            break
        a = 1

        if tokens[x] == "ASSIGNMENT":
            instance += 1
            if tokens[x-1][:4] == "VAR:":
                if not tokens.count(tokens[x-1]) > 1:
                    clean(x-1, x+1)
                    a = -1 # we remove -1 and a couple above so we will rescan from that point
                else:
                    currentVar = tokens[x-1]
                    counter = x+1
                    scopes = 0
                    usedInScope = 0
                    while counter < len(tokens):
                        if scopes < 0:
                            break
                        item = tokens[counter]
                        if item == currentVar:# or item == ("STR:"+currentVar[4:]):
                            usedInScope += 1
                        if item == "ASSIGN_FUNC":
                            pass
                        if item == "START_SCOPE":
                            scopes+=1
                        if item == "END_SCOPE":
                            scopes-=1
                        counter += 1
                    diff = tokens.count(currentVar)-usedInScope
                    if diff > 1:
                        clean(x-1, x+1)
                        a = -1
        elif tokens[x] == "ASSIGN_FUNC":
            if tokens.count(tokens[x+2]) > 1:
                i = x+10
                fname = tokens[x+2]
                usedInFunc = 0
                scopes = 0
                while i <= len(tokens):
                    if scopes < 0:
                        break
                    i+=1
                    if i >= len(tokens):
                        break

                    if tokens[i] == fname:
                        usedInFunc += 1
                    elif tokens[i] == "START_SCOPE":
                        scopes+=1
                    elif tokens[i] == "END_SCOPE":
                        scopes-=1
                diff = tokens.count(tokens[x+2])-usedInFunc
                if diff > 1:
                    x += 2
                    continue
            # ====================================================== #
            arg_len = 0
            while not tokens[x+arg_len] == "END_ARGS":
                arg_len += 1
            code_len = 1
            if tokens[x+arg_len+1] == "START_SCOPE":
                scopes = 0
                #while True :
                while scopes >= 0:
                    if scopes < 0:
                        break
                    item = tokens[x+arg_len+1+code_len]
                    if item == "START_SCOPE":
                        scopes+=1
                    elif item == "END_SCOPE":
                        scopes-=1
                    code_len += 1
            final = x+arg_len+code_len # the middle +1 broke thing doe
            clean(x, final)
            #a+=final
            a=0

        x += a
    if recur <= 0:
        return tokens
    else : return trashCollector(tokens, recur-1)
