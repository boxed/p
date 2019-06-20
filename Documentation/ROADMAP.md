# Roadmap of the development of p
### And how you can help it
p is not a finished project
and these are our goals in
the near, close and far
future.

## Structure of p
p consists of three parts:
- p-core
- p-config
- p-lanugages

### p-core
p-core is the director of the
other parts of p.
If you call `p <arguments>`,
you actually  first execute p-core,
which then calls other parts.

### p-config
p-config is executed with the `p config`
command.
Everything that affects your installation of p
is handeled here:
Usernames, installed [language packages](#p-languages),
location of command binaries, etc.

### p-languages
Languages are the most modular part of p,
there are just so many languages / project types.
So language support can be installed
with p-config.
Each language package provides some binaries
as commands, to be called by p-core.
And a way of detecting the project type.

### Near future (alpha phase)
Some goals here p already achives:

1. Parse arguments by this scheme: `p <language> <command>`
p takes these arguments:

| `language` | The project type                       |
|------------|----------------------------------------|
| `command`  | Command name specific to project type  |

Each command is a seperate executable and called by p
and provided with any arguments provided by the user behind `command`.
If p can auto detect the project type, it'll omit the `language` argument
and let `command` be the first argument.

2. Auto detect by txt or regex
Auto detecting the type of project in the working directory is one of the most important
features of p, to make p a usable progam.
This is part of every language package and thus p-language.
p has two ways to detect the project type:
1. Text matching
2. Regualar Expressions

p compares the project structure with these files in the language packages.
And if p could match them, p will limit the set of commands to the commands
in the language packages.
