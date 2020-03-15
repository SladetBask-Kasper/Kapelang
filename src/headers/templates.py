includes = """#include <iostream>
#include <sstream>
#include <stdio.h>
"""
defines = """

#define VER "0.2.5"
"""
funcs = """
void printVersion() {
using namespace std;
cout << "VERSION:" << VER << endl;
return;}\n
"""
maine = """
int main(int argc, char const *argv[]) {
using namespace std;
"""
