#include <iostream>
#include <fstream>
#include <string.h>
#include "config.h"

namespace P {
    class Process {
    private:
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

        // Execute Process
        int exec() {
            // Read .pconfig file
            std::string path;
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

        // Returns string of all output of one command
        std::string get_output_of_command(std::string command) {
            FILE *command_output = popen(command.c_str(),"r");
            long size = fsize(command_output);
            char* output = malloc(size);
            fread(output,size, size, command_output); // read all
            std::string output_str(output);
            return output_str;
        }

        // Test if path contains this->name package.
        // no alisases are resolved
        std::string find_language_package(std::string path) {
            std::string cmd = LS_CMD; // Reference for the ls-equivalent for the OS
            cmd += path;
            std::string dir_content = this->get_output_of_command(cmd); // Execute ls, to get directory structure
            if(dir_content.find(this->name) == std::string::npos) {
                return ""; // No package with this name available
            } else {
                // Full path of the language support package
                return path + PATH_DELIMTER + this->name;
            }
        }

        // Find command in package for language support.
        std::string find_command(std::string path) {
            // Read all
    };

    void printHelp() {
        std::cout << "Usage:\np <cmd> <args>" << std::endl;
    }
}
