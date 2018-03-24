#!/usr/bin/env python3

import os
from configparser import ConfigParser
from subprocess import check_output, CalledProcessError


def auto_detect_project_type(*, cmd_name, available_commands):
    prefix = f'{cmd_name}-projecttype-'
    commands = [x for x in available_commands if x.startswith(prefix)]

    possible_project_types = []

    for command in commands:
        try:
            check_output(command, shell=True)
            possible_project_types.append(command[len(prefix):])
        except CalledProcessError:
            pass

    possible_project_types = list(sorted(possible_project_types))
    for a, b in zip(possible_project_types, possible_project_types[1:]):
        if not b.startwith(a):
            raise Exception(f"Project types that aren't subtypes are not supported. It's not possible to disambiguate them. Found: '{a}' and '{b}'")

    return possible_project_types[-1]


def find_available_commands():
    r = []
    for path in os.environ["PATH"].split(os.pathsep):
        r.extend([x for x in os.listdir(path) if os.access(os.path.join(path, x), os.X_OK)])
    return set(r)


def alias_project_type(*, cmd_name, cmd, cfg):
    assert 'project_type' in cfg

    prefix, *command = cmd
    assert command[0] != cfg['project_type']

    assert prefix == cmd_name
    command = (cfg['project_type'], ) + tuple(command)

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
        r = _resolve_cmd(available_commands=available_commands, cmd=alias_project_type(cmd_name=cmd_name, cmd=cmd, cfg=cfg))

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
