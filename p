#!/usr/bin/env python3

import os
from configparser import ConfigParser
from subprocess import call

from p import find_available_commands, alias_and_resolve, auto_detect_project_type


def read_cfg(*, cmd_name):
    filename = '.%s-config' % cmd_name
    config = ConfigParser()
    config.read([filename, os.path.expanduser('~/' + filename)], encoding='utf8')
    r = dict(config.items('general'))
    if config.has_section('aliases'):
        r['aliases'] = dict(config.items('aliases'))
    if config.has_section('defaults'):
        r['defaults'] = dict(config.items('defaults'))
    return r


def main(argv):
    _, my_name = os.path.split(argv[0])
    cmd_name, _ = os.path.splitext(my_name)

    cfg = read_cfg(cmd_name=cmd_name)
    if 'project_type' not in cfg:
        detected_project_type = auto_detect_project_type(filenames=os.listdir('.'))
        if detected_project_type:
            cfg['project_type'] = detected_project_type

    available_commands = find_available_commands()
    command = alias_and_resolve(
        cmd_name=cmd_name,
        cmd=' '.join([cmd_name] + argv[1:]),
        available_commands=available_commands,
        cfg=cfg,
    )
    if command is None:
        print('Unknown command. Available commands:')
        for c in available_commands:
            if c.startswith('%s-' % cmd_name):
                print('\t', c)
    else:
        exit(call(command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr))


if __name__ == '__main__':
    import sys
    main(sys.argv)
