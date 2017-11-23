#!/usr/bin/env python3

import os
from subprocess import check_call

from p import find_available_commands, alias_and_resolve


def main(argv):
    _, my_name = os.path.split(argv[0])
    cmd_name, _ = os.path.splitext(my_name)
    available_commands = find_available_commands()
    command = alias_and_resolve(
        cmd_name=cmd_name,
        cmd=' '.join([cmd_name] + argv[1:]),
        available_commands=available_commands,
        cfg={},
    )
    if command is None:
        print('Unknown command. Available commands:')
        for c in available_commands:
            print('\t', c)
    else:
        check_call(command, shell=True)


if __name__ == '__main__':
    import sys
    main(sys.argv)
