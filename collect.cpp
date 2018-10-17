#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <cstdlib>

const unsigned CHUNK = 100;
struct lstruct {
    lstruct(size_t f, size_t t, const char* s) : from(f), to(t), str(s) {}
    size_t from, to;
    std::string str;
};

int main(int argc, char* argv[])
{
    std::ifstream lstrm("tmp.labels");
    std::vector<struct lstruct> labels;
    bool first = true, has_kraken_id = false;
    for (std::string line; std::getline(lstrm, line); ) {
        const char *p = line.c_str();
        //std::cerr << line << std::endl;
        size_t from = std::atoi(p);
        while (*++p != ' ') ;
        size_t to = std::atoi(++p);
        if (first) {
            first = false;
            const char* pp = p;
            while (*pp and *++pp != '|') ;
            if (*pp == '|')
                has_kraken_id = true;
        }
        if (has_kraken_id) {
            while (*++p != '|') ;
            while (*++p != '|') ;
        }
        else
            while (*++p != ' ') ;
        labels.emplace_back(from, to, p+1);
    }
    size_t n = labels.back().to;
    std::vector<bool> masked(n);
    for (std::string line; std::getline(std::cin, line); ) {
        if (line[0] == '>')
            masked.at(atoi(line.c_str()+2)) = true;
    }
    std::ifstream istrm("tmp.fa");
    size_t curr_label = 0;
    std::string masked_chunk, str;
    masked_chunk.assign(CHUNK, 'x');
    for (std::string line; std::getline(istrm, line); ) {
        if (line[0] == '>') {
            size_t curr_n = atoi(line.c_str()+2);
            std::getline(istrm, line);
            if (not masked[curr_n]) {
                if (curr_n == 0 or not masked[curr_n-1])
                    str += line.substr(0, CHUNK/2);
                else
                    str += masked_chunk.substr(0, CHUNK/2);
            }
            else {
                str += masked_chunk;
                if (curr_n+1 <= labels[curr_label].to) {
                    std::getline(istrm, line);
                    std::getline(istrm, line);
                    ++curr_n;
                }
            }
            if (curr_n == labels[curr_label].to) {
                if (str.find_first_of("AGCT") != std::string::npos) {
                    std::cout << ">" << labels[curr_label].str << "\n";
                    for (size_t i=0; i<str.size(); i+=60)
                        std::cout << str.substr(i, 60) << "\n";
                    std::cout << std::flush;
                }
                else
                    std::cerr << "Completely masked: " << labels[curr_label].str << std::endl;
                str.clear();
                ++curr_label;
            }
        }
    }
}
