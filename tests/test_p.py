import pytest

from p import validate_config, ConfigError, resolve_cmd, alias_and_resolve, alias, alias_once, alias_project_type, \
    apply_default, auto_detect_project_type, cmd_parts_into_node, Node


def test_alias_project_type():
    assert alias_project_type(cmd_name='p', cmd='p repl', cfg=dict(project_type='python')) == 'p python repl'

    assert alias_project_type(cmd_name='p', cmd='p python repl', cfg=dict(project_type='python')) == 'p python repl'

    assert alias_project_type(cmd_name='p', cmd='foo bar', cfg={}) == 'foo bar'


def test_alias_once1():
    assert 'p python repl' == alias_once(cmd_name='p', cmd='p repl', cfg=dict(project_type='python'))


def test_alias_once2():
    assert 'p python run manage.py shell' == alias_once(cmd_name='p', cmd='p repl', cfg=dict(project_type='python', aliases={'p python repl': 'p python run manage.py shell'}))


def test_alias_once3():
    assert 'p python run manage.py shell' == alias_once(cmd_name='p', cmd='p repl', cfg=dict(project_type='python', aliases={'p repl': 'p run manage.py shell'}))


def test_alias_once4():
    assert 'python manage.py shell' == alias_once(cmd_name='p', cmd='p python run manage.py shell', cfg=dict(project_type='python', aliases={'p python run': 'python'}))


def test_alias():
    assert 'python manage.py shell' == alias(cmd_name='p', cmd='p repl', cfg=dict(project_type='python', aliases={
        'p repl': 'p run manage.py shell',
        'p python run': 'python',
    }))


def test_resolve():
    assert resolve_cmd(available_commands=['p-new', ], cmd='p new python foo') == 'p-new python foo'
    assert resolve_cmd(available_commands=['p-new', 'p-new-python'], cmd='p new python foo') == 'p-new-python foo'
    assert resolve_cmd(available_commands=[], cmd='p new python foo') is None
    assert resolve_cmd(available_commands=['p-help', ], cmd='p help') == 'p-help'
    assert resolve_cmd(available_commands=[], cmd='foo/bar/baz') == 'foo/bar/baz'


def test_alias_and_resolve():
    assert 'python manage.py shell' == alias_and_resolve(cmd_name='p', cmd='p repl', available_commands=['python'], cfg=dict(project_type='python', aliases={'p repl': 'p run manage.py shell', 'p python run': 'python'}))


def test_validate_config():
    with pytest.raises(ConfigError):
        validate_config(cfg=dict(project_type=' foo bar'))

    with pytest.raises(ConfigError):
        validate_config(cfg=dict(aliases={'foo-bar': 'bar-baz'}))


def test_defaults():
    assert 'p-run foo' == apply_default(cmd_name='p', cmd='p-run', cfg=dict(defaults={'p run': 'foo'}))
    assert 'p-run foo' == apply_default(cmd_name='p', cmd='p-run', cfg=dict(project_type='python', defaults={'p run': 'foo'}))
    assert 'p-run foo' == alias_and_resolve(cmd_name='p', cmd='p run', available_commands=['p-run'], cfg=dict(defaults={'p run': 'foo'}))
    assert 'p-python-run foo' == alias_and_resolve(cmd_name='p', cmd='p run', available_commands=['p-python-run'], cfg=dict(project_type='python', defaults={'p run': 'foo'}))


def test_cmd_parts_into_node():
    root_node = Node(name='__root__')
    assert cmd_parts_into_node(root_node, ['p', 'run', 'foo']).name == 'foo'
    assert 'p' in root_node.children
    assert 'run' in root_node.children['p'].children
    assert 'foo' in root_node.children['p'].children['run'].children
    assert root_node.children['p'].parent == root_node
    assert root_node.children['p'].children['run'].parent == root_node.children['p']
    assert root_node.children['p'].children['run'].children['foo'].parent == root_node.children['p'].children['run']


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
        'LICENSE',
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
