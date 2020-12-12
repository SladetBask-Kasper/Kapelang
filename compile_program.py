from os import system
from sys import argv

if __name__ == "__main__":
    system(f"python3 /home/kada1004/pro/Kapelang/src/main.py {argv[1]} PAR > {argv[2]}.cpp")
    system(f"g++ {argv[2]}.cpp -o {argv[2]}.o")
    
