#!/usr/bin/env python3

import os
import re
from collections import defaultdict
from configparser import ConfigParser
from subprocess import check_output, CalledProcessError


def auto_detect_project_type(*, cmd_name, paths=None, txt_definitions=None, regex_definitions=None, available_commands=None):
    prefix = f'{cmd_name}-projecttype-'

    if available_commands is None:
        available_commands = find_available_commands(paths=paths)
    commands = [x for x in available_commands if x.startswith(prefix)]

    filenames = set(os.listdir('.'))

    if txt_definitions is None:
        txt_definitions = read_definitions(cmd_name=cmd_name, suffix='.txt', paths=paths)
    for key, definitions in sorted(txt_definitions.items(), reverse=True):
        for definition in definitions:
            if definition in filenames:
                return key

    if regex_definitions is None:
        regex_definitions = read_definitions(cmd_name=cmd_name, suffix='.regex', paths=paths)
    for key, definitions in regex_definitions.items():
        for definition in definitions:
            for filename in filenames:
                if re.match(definition, filename):
                    return key

    possible_project_types = []

    for command in commands:
        try:
            check_output(command, shell=True)
            possible_project_types.append(command[len(prefix):])
        except CalledProcessError:
            pass

    possible_project_types = list(sorted(possible_project_types))
    for a, b in zip(possible_project_types, possible_project_types[1:]):
        if not b.startswith(a):
            raise Exception(f"Project types that aren't subtypes are not supported. It's not possible to disambiguate them. Found: '{a}' and '{b}'")

    if possible_project_types:
        return possible_project_types[-1]
    else:
        return None


def find_available_commands(*, paths=[]):
    """
find_available_commands:
Arguments:
paths=[] : List of locations (str), in which to look for files to execute as commands.
    """
    if paths is None:
        paths = os.environ["PATH"].split(os.pathsep)
    r = []
    for path in paths.split(os.pathsep):
        try:
            r.extend(os.listdir(path))
        except FileNotFoundError:
            continue
    return set(r)


def read_definitions(*, cmd_name, suffix, paths=None):
    if paths is None:
        paths = os.environ["PATH"]
    r = defaultdict(set)
    prefix = f'{cmd_name}-projecttype-'
    assert suffix[0] == '.'
    for path in paths.split(os.pathsep):
        for filename in os.listdir(path):
            if filename.startswith(prefix) and filename.endswith(suffix) and not os.access(os.path.join(path, filename), os.X_OK):
                project_type = filename[len(prefix):-len(suffix)]
                with open(os.path.join(path, filename)) as f:
                    lines = {x.strip() for x in f.readlines()}
                    r[project_type] |= {x for x in lines if x}
    return r


def alias_project_type(*, cmd_name, cmd, project_type):
    prefix, *command = cmd
    assert command[0] != project_type

    assert prefix == cmd_name
    command = (project_type, ) + tuple(command)

    return (prefix, ) + command


def alias_once(*, cmd, cfg):
    if 'aliases' not in cfg:
        return cmd

    aliases = cfg['aliases']
    for c in reversed(range(1, len(cmd) + 1)):
        try_command = cmd[:c]
        if try_command in aliases:
            return aliases[try_command] + cmd[c:]
    return cmd


def alias(*, cmd_name, cmd, cfg):
    new_cmd = alias_once(cmd=cmd, cfg=cfg)
    if new_cmd == cmd:
        return cmd
    else:
        return alias(cmd_name=cmd_name, cmd=new_cmd, cfg=cfg)


def resolve_cmd(*, available_commands, cmd_name, cmd, cfg):
    validate_config(cfg=cfg)
    default = cfg.get('defaults', {}).get(cmd)

    r = None
    if 'project_type' in cfg:
        r = _resolve_cmd(available_commands=available_commands, cmd=alias_project_type(cmd_name=cmd_name, cmd=cmd, project_type=cfg['project_type']))

    if r is None:
        r = _resolve_cmd(available_commands=available_commands, cmd=cmd)

    if default:
        return f'{r} {default}'
    else:
        return r


def _resolve_cmd(*, available_commands, cmd):
    prefix, *command = cmd
    if '/' in prefix:
        return ' '.join(cmd)

    for c in reversed(range(1, len(command) + 1)):
        try_command = '-'.join([prefix] + command[:c])
        if try_command in available_commands:
            params = command[c:]
            return ' '.join([try_command] + params)

    if prefix in available_commands:
        return ' '.join([prefix] + command)

    if '_' in cmd[1]:
        return _resolve_cmd(available_commands=available_commands, cmd=(cmd[0], cmd[1].rpartition('_')[0]) + cmd[2:])

    return None


def alias_and_resolve(*, cmd_name, cmd, available_commands, cfg):
    if len(cmd) == 1:
        cmd += ('help', )

    assert isinstance(cmd, tuple)
    if cmd_name in available_commands:
        available_commands.remove(cmd_name)  # avoid circular lookup
    cmd = alias(cmd_name=cmd_name, cmd=cmd, cfg=cfg)
    return resolve_cmd(available_commands=available_commands, cmd_name=cmd_name, cmd=cmd, cfg=cfg)


class ConfigError(Exception):
    pass


def validate_config(*, cfg):
    if 'project_type' in cfg and ' ' in cfg['project_type']:
        raise ConfigError('project_type cannot contain spaces')
    if 'aliases' in cfg:
        aliases = cfg['aliases']

        for k in aliases:
            if not isinstance(k, tuple):
                raise ConfigError('Aliases must be tuples, %r is not' % k)

        for k in aliases.keys():
            if '-' in k[0]:
                raise ConfigError('Aliases should be written in the form "foo bar", not "fo-bar". Incorrect value "%s"' % k)
    if 'defaults' in cfg:
        for k in cfg['defaults'].keys():
            if '-' in k[0]:
                raise ConfigError('Defaults should be written in the form "foo bar", not "fo-bar". Incorrect value "%s"' % k)
            if not isinstance(k, tuple):
                raise ConfigError('Defaults must be tuples, %r is not' % k)


def read_cfg(*, cmd_name):
    filename = '.%s-config' % cmd_name
    config_parser = ConfigParser()
    config_parser.read([filename, os.path.expanduser('~/' + filename)], encoding='utf8')
    return parse_cfg(config_parser=config_parser)


def parse_cfg(*, config_parser):
    cfg = {}
    if config_parser.has_section('general'):
        cfg.update(dict(config_parser.items('general')))

    def parse_tuple_key_dict(key):
        if config_parser.has_section(key):
            d = {
                tuple(k.split(' ')): v
                for k, v in config_parser.items(key)
            }
            cfg[key] = d

    parse_tuple_key_dict('aliases')
    if 'aliases' in cfg:
        cfg['aliases'] = {k: tuple(v.split(' ')) for k, v in cfg['aliases'].items()}

    parse_tuple_key_dict('defaults')
    validate_config(cfg=cfg)
    return cfg
