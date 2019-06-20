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

1. Call other binaries for commands and give arguments

2. 