#!/usr/bin/env python3

import os
from subprocess import call

from p import find_available_commands, alias_and_resolve, auto_detect_project_type, read_cfg


RECURSION_DEPTH_ENVIRONMENT_VARIABLE = '_P_RECURSION_DEPTH'


def main(argv):
    _, my_name = os.path.split(argv[0])
    cmd_name, _ = os.path.splitext(my_name)

    available_commands = find_available_commands()

    cfg = read_cfg(cmd_name=cmd_name)
    if 'project_type' not in cfg:
        detected_project_type = auto_detect_project_type(cmd_name=cmd_name, available_commands=available_commands)
        if detected_project_type:
            cfg['project_type'] = detected_project_type

    recursion_depth = int(os.environ.get(RECURSION_DEPTH_ENVIRONMENT_VARIABLE, '0'))

    if recursion_depth > 50:
        print('ERROR: infinite loop detected')
        return -1

    command = alias_and_resolve(
        cmd_name=cmd_name,
        cmd=(cmd_name, ) + tuple(argv[1:]),
        available_commands=available_commands,
        cfg=cfg,
    )
    if command is None:
        if 'project_type' in cfg:
            print('Project type: %s' % cfg['project_type'])
        else:
            print('Unknown project type')
        print('Unknown command. Available commands:')
        for c in sorted(available_commands):
            if c.startswith(f'{cmd_name}-projecttype-'):
                continue
            if c.startswith(f'{cmd_name}-'):
                print('\t', c.replace('-', ' '))
    else:
        return call(
            command,
            shell=True,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            env={
                **os.environ,
                RECURSION_DEPTH_ENVIRONMENT_VARIABLE: str(recursion_depth + 1),
            },
        )


if __name__ == '__main__':
    import sys
    exit(main(sys.argv))
