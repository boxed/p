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


def alias_project_type(*, cmd_parts, cfg):
    assert 'project_type' in cfg
    if len(cmd_parts) > 1:
        assert cmd_parts[1] != cfg['project_type'], 'project_type should not be aliased up front'

    return [cmd_parts[0], cfg['project_type']] + cmd_parts[1:]


def alias_once(*, cmd_name, cmd, cfg):
    pass


def alias(*, cmd_name, cmd, cfg):
    new_cmd = alias_once(cmd_name=cmd_name, cmd=cmd, cfg=cfg)
    if new_cmd == cmd:
        return cmd
    else:
        return alias(cmd_name=cmd_name, cmd=new_cmd, cfg=cfg)


def resolve_cmd(*, available_commands, cmd):
    pass


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
