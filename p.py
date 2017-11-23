#!/usr/bin/env python3

import os


def find_available_commands():
    r = []
    for path in os.environ["PATH"].split(os.pathsep):
        r.extend([x for x in os.listdir(path) if os.access(x, os.X_OK)])

    return [x for x in r if x]


def alias_project_type(*, cmd_name, cmd, cfg):
    assert not cmd.startswith(cmd_name + '-')
    if not cmd.startswith(cmd_name + ' '):
        return cmd
    prefix, *command = cmd.split(' ')
    assert prefix == cmd_name
    if 'project_type' in cfg:
        if command and command[0] != cfg['project_type']:
            command = [cfg['project_type']] + command
    return ' '.join([prefix] + command)


def alias_once(*, cmd_name, cmd, cfg):
    aliases = {
        alias_project_type(cmd_name=cmd_name, cmd=k, cfg=cfg): alias_project_type(cmd_name=cmd_name, cmd=v, cfg=cfg)
        for k, v in cfg.get('aliases', {}).items()
    }
    cmd = alias_project_type(cmd_name=cmd_name, cmd=cmd, cfg=cfg)
    for k, v in aliases.items():
        if cmd.startswith(k):
            new_cmd = v + cmd[len(k):]
            return alias_project_type(cmd_name=cmd_name, cmd=new_cmd, cfg=cfg)
    return cmd


def alias(*, cmd_name, cmd, cfg):
    new_cmd = alias_once(cmd_name=cmd_name, cmd=cmd, cfg=cfg)
    if new_cmd == cmd:
        return cmd
    else:
        return alias(cmd_name=cmd_name, cmd=new_cmd, cfg=cfg)


def resolve_cmd(*, available_commands, cmd):
    prefix, *command = cmd.split(' ')
    for c in reversed(range(1, len(command) + 1)):
        try_command = '-'.join([prefix] + command[:c])
        if try_command in available_commands:
            params = command[c:]
            return ' '.join([try_command] + params)
    if prefix in available_commands:
        return ' '.join([prefix] + command)


def alias_and_resolve(*, cmd_name, cmd, available_commands, cfg):
    cmd = alias(cmd_name=cmd_name, cmd=cmd, cfg=cfg)
    return resolve_cmd(available_commands=available_commands, cmd=cmd)


class ConfigError(Exception):
    pass


def validate_config(*, cfg):
    if 'project_type' in cfg and ' ' in cfg['project_type']:
        raise ConfigError('project_type cannot contain spaces')
    if 'aliases' in cfg:
        aliases = cfg['aliases']
        for a in aliases.keys():
            if '-' in a:
                raise ConfigError('Aliases should be written in the form "foo bar", not "fo-bar". Incorrect value "%s"' % a)
