/*
    This is a file with a class for kabe::strings in c++ and kabe/kape -lang.
    I am not quite sure if I want to use this since it is kinda worsening the problems it is trying to solve.
    By that I mean, I sorta wanted a "catch-all" string to my programming language so you'll never need to deal
    with c string / std string conversion, but in trying to fix that I essentially just made everything worse.
    Because now we have c string / std string / kabe string conversion to worry about, which is quite bad.
    It also seems to be difficult dealing with arrays and conversion between for example
    std::vector<std::string> and std::vector<kabe::string>, and I could fix that by making for example
    a list class which inherits std::vector but wouldn't that just move the problem?

*/

#pragma once
#include <sstream>
#include <vector>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <boost/algorithm/string.hpp>

namespace kabe {
    class string : public std::string
    {
    public:
        using std::string::string;
        string(std::string x) {
            this->assign(x.data());
        }
        string(char x) { // idk why you can't already assign char to std::string, but here's a constructor for that anyways
            this->assign((char*)&x);
        }
        string(int x) { this->assign(std::to_string(x)); }
        string(float x) { this->assign(std::to_string(x)); }
        string(double x) { this->assign(std::to_string(x)); }
        string(bool x) {
            if (x == true) this->assign("true");
            else this->assign("false");
        }

        /// <summary>
        /// Naming convention taken from "std::string::c_str()".
        /// </summary>
        /// <returns>std::string copy of current kabe::string</returns>
        std::string std_str() {
            return std::string(this->c_str());
        }

        /// <summary>
        /// Trim from both ends
        /// </summary>
        /// <returns>kabe::string copy with heading and tailing whitespace removed</returns>
        string strip() {
            std::string str = this->std_str();
            boost::algorithm::trim(str);
            return string(str);
        }

        bool contains(string str) {
            std::string str1 = this->std_str();
            std::string str2 = str.std_str();

            return (str1.find(str2) != std::string::npos);
        }

        /// <summary>
        /// Replaces every mention of "from" with "to".
        /// </summary>
        /// <param name="from">What you want to replace</param>
        /// <param name="to">What you want in its' place</param>
        /// <returns>kabe::string copy with replace parts</returns>
        string replace(const std::string& from, const std::string& to) {
            std::string str = this->std_str();
            if (from.empty() || (str == ""))
                return string(str); // If it is empty then return an what was put in.}

            size_t start_pos = 0;
            while ((start_pos = str.find(from, start_pos)) != std::string::npos) {
                str.replace(start_pos, from.length(), to);
                start_pos += to.length(); // In case 'to' contains 'from', like replacing 'x' with 'yx'
            }
            return string(str);
        }

        string substring(int opt1, int opt2) {
            std::string value = this->std_str();
            int diff = 0;
            {
                int big = opt1;
                int small = opt2;
                if (opt1 < opt2) {
                    big = opt2;
                    small = opt1;
                }
                diff = big - small;
            }
            return value.substr(opt1, diff);
        }

        // Really this class should use s32 instead of int
        string manipulate(int opt1 = 0, int opt2 = 0) {
            string value = this->std_str();
            if (opt1 > opt2) {
                if (opt2 == 0) {
                    opt2 = value.length();
                }
            }
            if (opt1 < 0) opt1 = value.length() - (-opt1);
            if (opt2 < 0) opt2 = value.length() - (-opt2);
            return value.substring(opt1, opt2);
        }

        string upper() {
            std::string str = this->replace("ß", "SS").std_str();
            boost::to_upper(str);
            return string(str);
        }
        string lower() {
            std::string str = this->std_str();
            boost::to_lower(str);
            return string(str);
        }

        // https://www.techiedelight.com/convert-string-to-int-cpp/
        // can try/catch (std::invalid_argument const &e) or std::out_of_range for exceptions
        int toInt() {
            return std::stoi(this->std_str());
        }
        float toFloat() {
            return std::stof(this->std_str());
        }
        double toDouble() {
            return std::stod(this->std_str());
        }
        bool toBool(bool neither = false) {
            std::string str = this->lower().strip().std_str();
            if (str == "true") {
                return true;
            }
            else if (str == "false") {
                return false;
            }
            else {
                return neither; // perhaps there should be an exception thrown here instead?
            }
        }

        /// <summary>
        /// Solution based on: https://stackoverflow.com/a/14266139
        /// </summary>
        /// <param name="ch">the string you want to split at</param>
        /// <returns>std::vector of current string with split at each occurance of second string.</returns>
        std::vector<string> split(string ch) {
            std::string str = this->std_str();
            std::string delimiter = ch.std_str();
            std::vector<string> rv;

            size_t pos = 0;
            std::string token;
            while ((pos = str.find(delimiter)) != std::string::npos) {
                token = str.substr(0, pos);
                rv.push_back(token);
                str.erase(0, pos + delimiter.length());
            }
            rv.push_back(str); // This line was forgotten in original answer
            return rv;
        }

        /// <summary>
        /// Splits every time char appears in string
        /// </summary>
        /// <param name="ch">the char you want to split at</param>
        /// <returns>std::vector split at every "ch"</returns>
        std::vector<string> split(char ch)
        {
            const string txt = this->data();
            size_t pos = txt.find(ch);
            size_t initialPos = 0;
            std::vector<string> strs;
            strs.clear();

            // Decompose statement
            while (pos != std::string::npos) {
                strs.push_back(txt.substr(initialPos, pos - initialPos));
                initialPos = pos + 1;

                pos = txt.find(ch, initialPos);
            }

            // Add the last one
            strs.push_back(txt.substr(initialPos, std::min(pos, txt.size()) - initialPos + 1));
            return strs;
        }
    };
}
