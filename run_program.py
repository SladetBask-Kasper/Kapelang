from os import system

if __name__ == "__main__":
    system("python3 src/main.py src/inpfile.ka PAR > src/main.cpp")
    system("g++ src/main.cpp")
    print(f"\n{'_'*24}\nOutput:")
    system("./src/a.out")
