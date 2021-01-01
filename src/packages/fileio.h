#pragma once
#include <string>
#include <fstream>
#include <streambuf>

std::string readFile(std::string filenname) {
    std::ifstream t(filenname);
    std::string str;

    t.seekg(0, std::ios::end);
    str.reserve(t.tellg());
    t.seekg(0, std::ios::beg);

    str.assign((std::istreambuf_iterator<char>(t)),
                std::istreambuf_iterator<char>());
    return str;
}
