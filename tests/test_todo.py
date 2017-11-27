from p import alias_and_resolve


def test_fallback():
    assert 'p-new foo' == alias_and_resolve(
        cmd_name='p',
        cmd='p new foo',
        available_commands=['p-new'],
        cfg=dict(
            project_type='python',
            aliases={},
        )
    )

# This test causes an infinite loop in alias() right now
# def test_default():
#     assert 'p-run foo' == alias_and_resolve(
#         cmd_name='p',
#         cmd='p run',
#         available_commands=['p-pun'],
#         cfg=dict(
#             aliases={
#                 'p run': 'p run [foo]',
#             },
#         )
#     )


def auto_detect_project_type(filenames):
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

#
# def test_autodetect_c_sharp():  # .net generally?
#     assert 'c_sharp' == auto_detect_project_type(filenames=[
#     ])
#
#
# def test_autodetect_c():
#     assert 'c' == auto_detect_project_type(filenames=[
#     ])
#
#
# def test_autodetect_javascript():
#     assert 'javascript' == auto_detect_project_type(filenames=[
#     ])
#
#
# def test_autodetect_php():
#     assert 'php' == auto_detect_project_type(filenames=[
#     ])
#
#
# def test_autodetect_go():
#     assert 'go' == auto_detect_project_type(filenames=[
#     ])
