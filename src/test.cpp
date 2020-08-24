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
return;}

bool myFunc(int funcNum, std::string called)
{
std::cout << "This is function number "<<funcNum<<", also known as "<<called<<". That is #epic" << std::endl;if (funcNum == (int) 0)
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
bool myFunc2(int funcNum, std::string called)
{
std::cout << "This is function number "<<funcNum<<", also known as "<<called<<". That is #epic" << std::endl;if (funcNum == (int) 0)
{
return (bool) true;
}
else if (funcNum >= (int) 0)
{
return myFunc(funcNum-1, called);
}
else if (funcNum <= (int) 0)
{
return myFunc2(funcNum+1, called);
}
else
{
return (bool) false;
}

}

int main(int argc, char const *argv[]) {
using namespace std;
std::cout << "Hello, World!" << std::endl;int myVar = 13;printVersion();std::cout << ""<<VER<<"" << std::endl;myFunc(myVar, (std::string) "This be my func");return 0;}
