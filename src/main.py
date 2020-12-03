from sys import argv
import headers.lexer as lexer
import headers.parser as parser

if len(argv) < 2:
    argv.append("inpfile.ka")
    argv.append("PAR")
else:
    if argv[1] == "@": argv[1] = "inpfile.ka"
content = []
file = open(str(argv[1]), "r")
for l in file:
    line = str(l).strip()
    if line[:2] == "//": # doesn't read comments into memory again
        continue         # NOTE : I will not be able to tell coder which line error is on
    if line == "":
        continue
        print("rip")
    if "//" in line:
        line = str(line.split("//")[0].strip())
    content.append(line)
del file

if __name__ == "__main__":
    # Main func
    lex = lexer.lexer(content)
    arg = "SHOWLEX"
    try:
        arg = argv[2]
    except:pass
    if arg == "SHOWLEX" or arg == "LEX":
        print(lex)
    elif arg == "SHOWPAR" or arg == "SHOWPARSE" or arg == "PARSE" or arg == "PAR":
        par = parser.parser(lex).replace("\#", "#")
        print(par.replace(";", ";\n"))
        #print(par)
    elif arg == "NEUTRAL" or arg == "NEU":
        par = parser.parser(lex)
        print("DONE.")
        exit()
