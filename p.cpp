#include <iostream>
#include "p.h"
using namespace P;

int main(int argc,char* argv[]) {
    if(argc < 3) { // anything that doesn't follow this scheme: p <name> <cmd>, needs to printHelp()
        printHelp(); // **TODO** Implement auto detect to also use this scheme p <cmd>
    }
    Process process = Process(argc-1,&argv[1]);//ignore argv[0], because argv[0] == "p".
    process.exec();
}
