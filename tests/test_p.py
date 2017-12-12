from configparser import ConfigParser

import pytest

from p import validate_config, ConfigError, resolve_cmd, alias_and_resolve, alias, alias_once, alias_project_type, \
    auto_detect_project_type, parse_cfg


def test_alias_project_type():
    assert alias_project_type(cmd_name='p', cmd=('p', 'repl'), cfg=dict(project_type='python')) == ('p', 'python', 'repl')

    with pytest.raises(AssertionError):
        # alias already applied
        alias_project_type(cmd_name='p', cmd=('p', 'python', 'repl'), cfg=dict(project_type='python'))

    with pytest.raises(AssertionError):
        # no project_type
        alias_project_type(cmd_name='p', cmd=('foo', 'bar'), cfg={})


def test_alias_once1():
    assert ('p', 'repl') == alias_once(cmd=('p', 'repl'), cfg=dict())


def test_alias_once2():
    assert ('p', 'run', 'manage.py', 'shell') == alias_once(cmd=('p', 'repl'), cfg=dict(aliases={('p', 'repl'): ('p', 'run', 'manage.py', 'shell')}))


def test_alias_once3():
    assert ('p', 'run', 'manage.py', 'shell') == alias_once(cmd=('p', 'repl'), cfg=dict(aliases={('p', 'repl'): ('p', 'run', 'manage.py', 'shell')}))


def test_alias_once4():
    assert ('python', 'manage.py', 'shell') == alias_once(cmd=('p', 'python', 'run', 'manage.py', 'shell'), cfg=dict(aliases={('p', 'python', 'run'): ('python',)}))


def test_alias():
    assert ('python', 'manage.py', 'shell') == alias(cmd_name='p', cmd=('p', 'repl'), cfg=dict(aliases={
        ('p', 'repl'): ('p', 'run', 'manage.py', 'shell'),
        ('p', 'run'): ('python', ),
    }))


def test_resolve():
    assert resolve_cmd(available_commands=['p-new', ], cmd_name='p', cmd=('p', 'new', 'python', 'foo'), cfg={}) == 'p-new python foo'
    assert resolve_cmd(available_commands=['p-new', 'p-new-python'], cmd_name='p', cmd=('p', 'new', 'python', 'foo'), cfg={}) == 'p-new-python foo'
    assert resolve_cmd(available_commands=[], cmd_name='p', cmd=('p', 'new', 'python', 'foo'), cfg={}) is None
    assert resolve_cmd(available_commands=['p-help', ], cmd_name='p', cmd=('p', 'help'), cfg={}) == 'p-help'
    assert resolve_cmd(available_commands=[], cmd_name='p', cmd=('foo/bar/baz', ), cfg={}) == 'foo/bar/baz'


def test_alias_and_resolve():
    assert 'python manage.py shell' == alias_and_resolve(cmd_name='p', cmd=('p', 'repl'), available_commands=['python'], cfg=dict(aliases={('p', 'repl'): ('p', 'run', 'manage.py', 'shell'), ('p', 'run'): ('python', )}))


def test_validate_config():
    with pytest.raises(ConfigError):
        validate_config(cfg=dict(project_type=' foo bar'))

    # internal data model tests
    with pytest.raises(ConfigError):
        validate_config(cfg=dict(aliases={'foo-bar': 'bar-baz'}))

    with pytest.raises(ConfigError):
        validate_config(cfg=dict(defaults={'foo-bar': 'bar-baz'}))

    # config file is invalid
    with pytest.raises(ConfigError):
        validate_config(cfg=dict(aliases={('foo-bar',): 'bar-baz'}))

    with pytest.raises(ConfigError):
        validate_config(cfg=dict(defaults={('foo-bar',): 'bar-baz'}))


def test_parse_cfg():
    config_parser = ConfigParser()
    config_parser.read_string("""
[general]
project_type=python

[aliases]
p foo=p bar
p baz=p quux

[defaults]
p foo=asd
    """.strip())
    assert parse_cfg(config_parser=config_parser) == {
        'project_type': 'python',
        'aliases': {
            ('p', 'baz'): 'p quux',
            ('p', 'foo'): 'p bar',
        },
        'defaults': {
            ('p', 'foo'): 'asd',
        },
    }



def test_defaults():
    assert 'p-run foo' == alias_and_resolve(cmd_name='p', cmd=('p', 'run'), available_commands=['p-run'], cfg=dict(defaults={('p', 'run'): 'foo'}))
    assert 'p-run foo' == alias_and_resolve(cmd_name='p', cmd=('p', 'run'), available_commands=['p-run'], cfg=dict(defaults={('p', 'run'): 'foo'}))
    assert 'p-python-run foo' == alias_and_resolve(cmd_name='p', cmd=('p', 'run'), available_commands=['p-python-run'], cfg=dict(project_type='python', defaults={('p', 'run'): 'foo'}))


def test_fallback_to_non_project_specific_command():
    assert 'p-new foo' == alias_and_resolve(
        cmd_name='p',
        cmd=('p', 'new', 'foo'),
        available_commands=['p-new'],
        cfg=dict(
            project_type='python',
            aliases={},
        )
    )


def test_autodetect_python():
    assert 'python' == auto_detect_project_type(filenames=[
        'docs/',
        'examples/',
        'lib/',
        'tests/',
        '.coveragerc',
        '.gitignore',
        '.travis.yml',
        'AUTHORS.rst',
        'CONTRIBUTING.rst',
        'HISTORY.rst',
        'LICENSE	tri',
        'MANIFEST.in',
        'Makefile',
        'README.rst',
        'TODO',
        'doc_output.py',
        'doc_viewer.html',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        'table.css',
        'table.scss',
        'table_example_1.png',
        'test_requirements.txt',
        'tox.ini',
        'venv_requirements.txt',
    ])


def test_autodetect_elm():
    assert 'elm' == auto_detect_project_type(filenames=[
        'src/',
        'tests/',
        '.gitignore',
        '.travis.yml',
        'LICENSE',
        'README.md',
        'elm-package.json',
    ])


def test_autodetect_clojure():
    assert 'clojure' == auto_detect_project_type(filenames=[
        'config/',
        'pkg/',
        'resources/',
        'src/',
        'tasks/',
        'test/',
        '.gitignore',
        '.lein-classpath',
        '.travis.yml',
        'CHANGES.markdown',
        'CONTRIBUTING.markdown',
        'LICENSE',
        'README.markdown',
        'project.clj',
    ])


def test_autodetect_swift():
    assert 'swift' == auto_detect_project_type(filenames=[
        'Alamofire.xcodeproj/',
        'Alamofire.xcworkspace/',
        'Documentation/',
        'Example/',
        'Source/',
        'Tests/',
        'docs/',
        '.gitignore',
        '.jazzy.yaml',
        '.ruby-gemset',
        '.ruby-version',
        '.swift-version',
        '.travis.yml',
        'Alamofire.podspec',
        'CHANGELOG.md',
        'CONTRIBUTING.md',
        'Gemfile',
        'Gemfile.lock',
        'ISSUE_TEMPLATE.md',
        'LICENSE',
        'PULL_REQUEST_TEMPLATE.md',
        'Package.swift',
        'README.md',
        'alamofire.png',
    ])


def test_autodetect_java():
    assert 'java' == auto_detect_project_type(filenames=[
        '.buildscript/',
        '.github/',
        'benchmarks/',
        'mockwebserver/',
        'okcurl/',
        'okhttp-android/',
        'okhttp-apache/',
        'okhttp-hpacktests/',
        'okhttp-logging/',
        'okhttp-testing/',
        'okhttp-tests/',
        'okhttp-urlconnection/',
        'okhttp/',
        'samples/',
        'website/',
        '.gitignore',
        '.gitmodules',
        '.travis.yml',
        'BUG-BOUNTY',
        'CHANGELOG.md',
        'LICENSE.txt',
        'README.md',
        'checkstyle.xml',
        'deploy_website.sh',
        'pom.xml',
    ])
