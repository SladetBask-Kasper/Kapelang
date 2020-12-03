includes = """#include <iostream>
#include <sstream>
#include <stdio.h>
"""
defines = """
#define VER "0.2.6"
"""
globals = """
"""
funcs = """
void printVersion() {
    using namespace std;
    cout << "VERSION:" << VER << endl;
    return;}
std::string input(std::string txt = "")
{
\tstd::string rv;\tstd::cin >> rv;\treturn rv;}
void error(const char *msg)
{
    perror(msg);
    exit(1);
}\n
"""
maine = """
int main(int argc, char const *argv[]) {
using namespace std;
"""
packages = "/home/kada1004/pro/Kapelang/src/packages/"
