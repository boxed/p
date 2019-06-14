#include <iostream>
#include <fstream>
#include <filesystem>
#include "config.h"

namespace P {
    class Process {
        char* name; // name used to refer on the commandline  (p <name> <cmd>)
        char** args;
        int argc;
    public:
        Process (int argc,char** argv) {
            // argv[0] = <name>
            // Everything else in argv[] = <args> for the cmd.
            this->name = argv[0]; // Language name
            this->args = &argv[1];
            this->argc = argc -1;
        }

        int exec(); // Execute Process
        std::string find_language_package(std::string); // Find path of language package in path, that matches this->name
        std::string find_command(std::string); // Find path to command resolve aliases

        // Execute Process
        int exec() {
            // Read .pconfig file
            std::string line;
            std::ifstream pconfig(LOCATION_P_CONFIG, std::ios::out);
            if (!pconfig.is_open()) {
                std::cerr << "Error: Unable to open settings file \"" << LOCATION_P_CONFIG << "\" for read" << std::endl;
                return false;
            }
            while ( std::getline(pconfig,path) ) {
                // Find path of language package
                std::string language_path = this->find_language_package(path);
                if( language_path != "") {
                    // Find path to command and resolve aliases
                    std::string command = this->find_command(language_path);
                    // Execute command
                    std::cout << command << std::endl;
                }
            }
            pconfig.close();
        }

        // Find path of language package in path, that matches this->name.
        std::string find_language_package(std::string path) {
            std::string cmd = LS_CMD; // Reference for the ls-equivalent for the OS
            cmd += path;
            FILE *path_content = popen(cmd.c_str(),"r"); // Execute ls, to get directory structure
            fsancf(path_content,this->name,path_package);

        }
    };

    void printHelp() {
        std::cout << "Usage:\np <cmd> <args>" << std::endl;
    }
}
