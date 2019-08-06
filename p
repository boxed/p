#! $(/usr/bin/which perl)

# My default installation of perl
use v5.024.1;

# Perl can easily dispatch other programs with the `cat` operator
# and capture their stdout with a simple assignment as a string:
# $cat_output = `cat LICENSE` # Read LICENSE into $cat_output


my $language = shift @ARGV;
my $command = shift @ARGV;
my $home_dir = `echo \$HOME`; # There must be a better way to do this, will find out soon.
chomp $home_dir;

# Command to execute subcommand,
# no lookup of anything in the PATH or current Directory on the same name yet.
my $dispatchable_command = "$home_dir/.p/packages/$language/$command";


my $output = `$dispatchable_command`;
print "Output:$output";

