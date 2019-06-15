#include <stdio.h>
#include <string.h>
#include "p.h"

int main(void) {
    // Init p_process struct
    p_process process = {
        .commands = getCommands() // Get acknowledged Packages from .pconfig paths
    };
