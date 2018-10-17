#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

const unsigned CHUNK = 100;

int main()
{
    std::string str, label;
    std::vector<std::string> s;
    bool read_started = false;
    size_t n = 0;
    std::ofstream ostrm("tmp.fa");
    for (std::string line; std::getline(std::cin, line); ) {
        if (line[0] == '>') {
            std::cout << n << " ";
            if (read_started) {
                for (size_t p=0; p<str.size(); p+=CHUNK/2) {
                    ostrm << ">N" << n << std::endl;
                    ostrm << str.substr(p, CHUNK) << std::endl;
                    ++n;
                }
                std::cout << n-1 << " " << label.c_str()+1 << std::endl;
                str.clear();
                s.clear();
            }
            label = line;
            continue;
        }
        str += line;
        read_started = true;
    }
}
