#include <iostream>
#include <sstream>
#include <stdio.h>
#include <string.h>

#define VER "0.2.6"
#define DAMN "Daniel"
#define KASBURGER "Resturant at 18 boardwalk avenue"
#define aao "åäö"


void printVersion() {
    using namespace std;

    cout << "VERSION:" << VER << endl;

    return;
}
std::string input(std::string txt = "")
{
	std::string rv;
	std::cin >> rv;
	return rv;
}
void error(const char *msg)
{
    perror(msg);

    exit(1);

}

bool myFunc(int funcNum, std::string called)
{
std::cout << "This is function number "<<funcNum<<", also known as "<<called<<". That is #epic" << std::endl;
if (funcNum == (int) 0)
{
return (bool) true;

}
else if (funcNum >= (int) 0)
{
return myFunc(funcNum-1, called);

}
else if (funcNum <= (int) 0)
{
return myFunc(funcNum+1, called);

}
else
{
return (bool) false;

}

}

int main(int argc, char const *argv[]) {
using namespace std;

std::cout << "Hello, World!" << std::endl;
int myVar = 13;
std::string name = "Kape";
int funnySexNumber = 69;
printVersion();
std::cout << ""<<VER<<"" << std::endl;
myFunc(myVar, (std::string) "This be my func");
return 0;
}
