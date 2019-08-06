#! /usr/bin/perl -w

use v5.010;

# Perl can easily dispatch other programs with the `cat` operator
# and capture their stdout with a simple assignment as a string:
# $cat_output = `cat LICENSE` # Read LICENSE into $cat_output


$language = shift @ARGV;
$command = shift @ARGV;
chomp $home_dir;

# Command to execute subcommand,
# no lookup of anything in the PATH or current Directory on the same name yet.
$dispatchable_command = "~/.p/packages/$language/$command";


`$dispatchable_command`;
