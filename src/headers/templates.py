includes = """#include <iostream>
#include <sstream>
#include <stdio.h>
"""
defines = """
#define VER "0.1.4"
"""
funcs = """
void printVersion() {
using namespace std;
cout << "VERSION:" << VER << endl;
return;}
"""
maine = """

int main(int argc, char const *argv[]) {
using namespace std;
"""
