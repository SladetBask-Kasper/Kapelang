#pragma once
#include <fstream>
#include <streambuf>
#include <vector>
#include "stdkabe.h"

namespace kabe {
    class FileReader {
    protected:
        kabe::string content = "";

        /// <summary>
        /// Reads file to std::String which can then be converted to kabe::string
        /// An issue with this approach is that it will not work with big files.
        /// Perhaps i might look at the python "readline()" method for inspiration.
        /// </summary>
        /// <param name="filenname">Full path to file</param>
        /// <returns>kabe::string with complete file content.</returns>
        kabe::string readFile(kabe::string filenname) {
            std::ifstream t(filenname);
            std::string str;

            t.seekg(0, std::ios::end);
            str.reserve((size_t)t.tellg());
            t.seekg(0, std::ios::beg);

            str.assign((std::istreambuf_iterator<char>(t)),
                std::istreambuf_iterator<char>());
            return str;
        }
    public:
        FileReader(kabe::string path) {
            this->content = this->readFile(path);
        }
        kabe::string getContent() {
            return content;
        }
        std::vector<kabe::string> getLines() {
            return content.split('\n');
        }

    };
}