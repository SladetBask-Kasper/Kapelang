/*

    This dict (dictionary) class is written by "Kasper - Sladetbask" on github.
    (https://github.com/SladetBask-Kasper/)
    Note: this is taken from (https://github.com/SladetBask-Kasper/klib-cpp/blob/master/klib/dict.h)
    and is not original to Kabelang.

*/
#pragma once
#include <string>
#include <vector>
#include <algorithm>
#include "stdkabe.h"

#define DICT_GET_ERROR "Get Error (from dict)"

/*

    This class is a class that was made to bring python dictionary (Dict) to C++
    The class is writen on windows but should work on any platform!

    [HOW IT WORKS]
    It takes two vectors and assings a value and a name two each vector,
    then when it trys to get the vectors value, because we assign a value and refrence name at the same time,
    the refrence name and value have the same index!

    [FOR PEOPLE WHO WILL READ THE SOURCE CODE]
    refrence = the vector with names
    value    = Is in most cases the content of the dict. (Edit: What do I mean "most cases?")

*/
namespace kabe {
    class dict {
    protected:
        std::vector<kabe::string> mainVector;
        std::vector<kabe::string> refrenceVector;
    public:
        bool append(kabe::string, kabe::string);
        dict(kabe::string, kabe::string);
        dict();
        virtual ~dict() {};

        int scanIndex(kabe::string);
        kabe::string get(kabe::string);
        std::vector<kabe::string> get(int pos);
        size_t length();
        size_t size();
        bool removeValue(kabe::string);
        bool changeValue(kabe::string, kabe::string);
        bool isValue(kabe::string allocName);
        bool isEmpty();
        bool move(kabe::string, kabe::string);

    };
    }

    /*
        constructor...
    */
    kabe::dict::dict(kabe::string allocName, kabe::string content) {
        append(allocName, content);
    }
    kabe::dict::dict() {}

    /*
        Appends to the vectors
        adding the refrence along with its value
    */
    bool kabe::dict::append(kabe::string allocName, kabe::string content) {

        if (!refrenceVector.empty()) {
            for (size_t i = 0; i < refrenceVector.size(); i++) {
                if (refrenceVector[i] == allocName) {
                    return false;
                }
            }
        }

        // mainVector Holds Content
        mainVector.push_back(content);
        refrenceVector.push_back(allocName);

        return true;
    }

    /*
        scans for the value, getting the index value!
    */
    int kabe::dict::scanIndex(kabe::string valueToScanFor) {
        for (size_t i = 0; i < refrenceVector.size(); i++) {
            if (refrenceVector[i] == valueToScanFor) {
                return i;
            }
        }
        return -1;
    }

    /*
        Gets the value of refrence
    */
    kabe::string kabe::dict::get(kabe::string allocName) {

        int callIndex = scanIndex(allocName);
        if (callIndex == -1) {
            return DICT_GET_ERROR;
        }
        return mainVector[callIndex];
    }
    std::vector<kabe::string> kabe::dict::get(int pos) {
        std::vector<kabe::string> rv;
        rv.push_back(refrenceVector[pos]);
        rv.push_back(mainVector[pos]);
        return rv;
    }

    /*
        Gets length of vector
    */
    size_t kabe::dict::length() {
        return refrenceVector.size();
    }
    size_t kabe::dict::size() {
        return this->length(); // couldn't decide what to call it so..
    }

    /*

        Removes a value from the thingy

    */

    bool kabe::dict::removeValue(kabe::string allocName) {
        int callIndex = scanIndex(allocName);
        if (callIndex == -1) {
            return false;
        }

        mainVector.erase(mainVector.begin() + callIndex);
        refrenceVector.erase(refrenceVector.begin() + callIndex);

        return true;
    }

    /*

        Checks if value exists.

    */

    bool kabe::dict::isValue(kabe::string allocName) {
        return (scanIndex(allocName) != -1);
    }

    /*

        if dict is empty

    */
    bool kabe::dict::isEmpty() {
        return refrenceVector.empty();
    }

    /*

        Allows you to change the value of a refrence

    */
    bool kabe::dict::changeValue(kabe::string fromNAME, kabe::string toCONTENT) {
        int id = scanIndex(fromNAME);

        if (id == -1) {
            return false;
        }

        mainVector[id] = toCONTENT;
        return true;
    }

    /*

        Moves the value from a refrence to another

    */
    bool kabe::dict::move(kabe::string fromNAME, kabe::string toNAME) {

        int id = scanIndex(fromNAME);
        int id2 = scanIndex(toNAME);

        kabe::string flags = "";

        if (id == -1) {
            return false;
        }
        if (id2 == -1) {
            flags = flags + "MAKENEW ";
        }

        if (flags.find("MAKENEW") != kabe::string::npos) {
            // if we gonna make new
            append(toNAME, mainVector[id]);// id = fromNAME id
            return true;
        }
        else {
            // or not
            refrenceVector[id] = mainVector[id2];
            return true;
        }

}