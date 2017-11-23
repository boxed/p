import pytest

from p import validate_config, ConfigError, resolve_cmd, alias_and_resolve, alias, alias_once, alias_project_type


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


def test_alias_and_resolve():
    assert 'python manage.py shell' == alias_and_resolve(cmd_name='p', cmd='p repl', available_commands=['python'], cfg=dict(project_type='python', aliases={'p repl': 'p run manage.py shell', 'p python run': 'python'}))


def test_validate_config():
    with pytest.raises(ConfigError):
        validate_config(cfg=dict(project_type=' foo bar'))

    with pytest.raises(ConfigError):
        validate_config(cfg=dict(aliases={'foo-bar': 'bar-baz'}))
