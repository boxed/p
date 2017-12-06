#!/usr/bin/env python3

import os
from typing import List


def auto_detect_project_type(*, filenames):
    simple_filename_tells = dict(
        python='requirements.txt',
        elm='elm-package.json',
        clojure='project.clj',
        swift='Package.swift',
        java='pom.xml',
    )
    for language, filename in simple_filename_tells.items():
        if filename in filenames:
            return language


def find_available_commands():
    r = []
    for path in os.environ["PATH"].split(os.pathsep):
        r.extend([x for x in os.listdir(path) if os.access(os.path.join(path, x), os.X_OK)])
    return set(r)


class Node:
    def __init__(self, *, parent=None, name: str, defaults: str=None, children=None):
        self.parent = parent
        self.name = name
        self.defaults = defaults
        self.children = children or {}

    def __repr__(self):
        return f'Node({self.name})'


def cmd_parts_into_node(root_node: Node, cmd_parts: List[str]) -> Node:
    i = root_node
    for part in cmd_parts:
        if part not in i.children:
            i.children[part] = Node(name=part, parent=i)
        i = i.children[part]
    return i


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
        alias_project_type(cmd_name=cmd_name, cmd=k, cfg=cfg): apply_default(cmd_name=cmd_name, cmd=alias_project_type(cmd_name=cmd_name, cmd=v, cfg=cfg), cfg=cfg)
        for k, v in cfg.get('aliases', {}).items()
    }
    cmd = alias_project_type(cmd_name=cmd_name, cmd=apply_default(cmd_name=cmd_name, cmd=cmd, cfg=cfg), cfg=cfg)
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
    if '/' in prefix:
        return cmd
    for c in reversed(range(1, len(command) + 1)):
        try_command = '-'.join([prefix] + command[:c])
        if try_command in available_commands:
            params = command[c:]
            return ' '.join([try_command] + params)
    if prefix in available_commands:
        return ' '.join([prefix] + command)


def apply_default(*, cmd_name, cmd, cfg):
    if cmd is None:
        return None
    cmd_with_project_type = alias_project_type(cmd_name=cmd_name, cmd=cmd.replace('-', ' '), cfg=cfg)
    default = cfg.get('defaults', {}).get(cmd_with_project_type, None)
    if default is None and cmd_with_project_type != cmd:
        default = cfg.get('defaults', {}).get(cmd.replace('-', ' '), None)
        return f'{cmd} {default}' if default else cmd
    else:
        return f'{cmd} {default}' if default else cmd


def alias_and_resolve(*, cmd_name, cmd, available_commands, cfg):
    if cmd_name in available_commands:
        available_commands.remove(cmd_name)  # avoid circular lookup
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
