# p (for project)

Most languages have nice tools like this:

```
> somecommand new foo
> cd foo
> somecommand test
Creating isolated environment 
Installing dependencies
Tested ok!
```

...but what is that `somecommand`? For elm it's easy, it's `elm`, but for rust it's `cargo` and for Clojure it's `lein`. For some languages there are more than one you need to know about or multiple separate tools that do parts of this.

P is the tool to put that under one roof.

To accomplish this daring goal we must:

- auto detect language (and project type!) in most cases and be super easily configurable in cases where we don't detect automatically 
- auto detect our e vironment so we can know how to install required tools
- have an open architecture so implementating support for a language can be done_in that language_ and not force everyone into writing javascript or bash or whatever
- have an open community so we can have implementations for even very small languages made by the people who knows them
- expose all the underlying power of the tools we are shadowing so we don't just get the least common denominator
- be shorter to write than the original tools (by having the hybris of taking a one character command name for example!)

