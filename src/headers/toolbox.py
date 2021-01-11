import re

def getBetween(str, str1, str2):
    pattern = str1+"(.*)"+str2
    compiled = re.compile(pattern)

    #ms = compiled.search(fbhandle.read())
    ms = compiled.search(str)
    return ms.group(1).strip()

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
        return "kabe::string"
    elif datatype == "CAST_L":
        return "long"
    elif datatype == "CAST_F":
        return "float"
    elif datatype == "CAST_D":
        return "double"
    elif datatype == "CAST_U8":
        return "u8"
    elif datatype == "CAST_S8":
        return "s8"
    elif datatype == "CAST_U16":
        return "u16"
    elif datatype == "CAST_S16":
        return "s16"
    elif datatype == "CAST_U32":
        return "u32"
    elif datatype == "CAST_S32":
        return "s32"
    elif datatype == "CAST_U32":
        return "u32"
    elif datatype == "CAST_S32":
        return "s32"
    elif datatype == "CAST_VOID":
        return "void"
    elif datatype[:6] == "CAST_V":
        return "std::vector" + datatype[7:]
    else:
        return datatype
    # ======= END OF TYPES ======= #

def datatype_to_c(data):
    if data[:4] == "STR:":
        return str(f"(kabe::string) \"{data[4:]}\"")
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
        rv = str(f"{data[10:]}")
        if data[-2:] == "()":
            return rv
        else:
            return rv+"()"
    else:
        return data

def trans(data):
    do_nothing_types = ["INT:", "VAR:", "LONG:", "BOOL:", "FLOAT:",
        "DOUBLE:"]
    if len(data) <= 4:
        return data
    elif data[:4] == "STR:":
        return str(f'"{data[4:]}"')
    elif data[:4] in do_nothing_types:
        return data[4:]
    elif len(data) <= 5: # ===========
        return data
    elif data[:5] in do_nothing_types:
        if data[:5] == "BOOL:":
            return data[5:].lower()
        return data[5:]
    elif len(data) >= len("FUNC_NAME:"):
        if data[:10] == "FUNC_NAME:":
            return data[10:]+"()"
    elif len(data) > 10:
        return data[10:]
    else:
        return data
