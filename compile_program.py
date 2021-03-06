from os import system
from sys import argv
from src.headers.templates import packages as pack
from src.headers.templates import src_path as src

if __name__ == "__main__":
    if not argv[1] == "COMPILE":
        system(f"python3 {src}main.py {argv[1]} PAR > {argv[2]}.cpp")
    system(f"g++ -std=c++17 -I{pack} {argv[2]}.cpp -o {argv[2]}.o")
