# User Guide for p, the genral project manager
Many languages have their own project manager.
Some examples are cargo for rust, elm for elm,
lein for clojure,
you name it.

But did you ever try to use cargo as
you use elm?
You can't use one project manager as
you use another one.

This adds extra challenges to
learning a new language.
An unnecessary challenge, I think.

## Install

p works on:

| OS    | Version of Python | Other requirements |
|-------|-------------------|--------------------|
| Linux | >Python 3.7.3     | None               |
|       |                   |                    |


You have to have Python 3.7.3 installed in the default
location ( no altinstall ).
Clone or download [this repository](https://github.com/boxed/p.git)
and add the location of p to your PATH variable.
Then go to a Python or Swift project and
type:
```bash
p
```
You'll be greeted with usage information about these commands.

## Most common commands

This is the general form of a p command:
```bash
p <language> <cmd>
```
If `p` can, it will detect the type
of your project,
and you can omit the <language> part.

Currently these are the basic commands that
you can use with python.

- [`p python env_path`](#python-env_path)
- [`p python install`](#python-install)
- [`p python install requirements hashes cache`](#python-install-requirements-hashes-cache)
- [`p python repl`](#python-repl)
- [`p python run`](#python-run)
- [`p python test`](#python-test)
- [`p python uninstall`](#python-unistall)

### `python env_path`
Prints the name of the hidden [virtualenv](https://virtualenv.pypa.io/en/stable/) directory,
p always uses a isolated version of python and pip, virtualenv is used by all commands
in p with python.

### `python install`
Install module from PyPi or other sources, you can provide
the same arguments to `p install` as to `pip install`, with
the only difference being that `p install` installs in the virtualenv python
of your project and `pip install` installs into your computers version of python.

### `python install requirements hashes cache`
**TODO**

### `python repl`
Open Python repl from virtualenv.

### `python run`
Run python file with virtualenv python.

### `python test`
Run pytest

### `python uninstall`
Uninstall package you installed via [`p python install`](#python-install)
