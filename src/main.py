from sys import argv
import headers.lexer as lexer
import headers.parser as parser

if len(argv) < 2:
    argv.append("inpfile.ka")
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
    par = parser.parser(lex)
    print(lex)
    #print(par)
