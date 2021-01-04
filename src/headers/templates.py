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
void error(const char *msg)
{
perror(msg);    exit(1);}
"""
maine = """
int main(int argc, char const *argv[]) {
using namespace std;
"""
packages = "/home/kada1004/pro/Kapelang/src/packages/"
