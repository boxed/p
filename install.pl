#!/usr/bin/env perl
# Create link with ln from  ~/.p to ./.p

my $default_dir = "\$HOME/.p" if !$ARGV[0] else $ARGV[0]; # Provide alternative destination for .p files
my $method = "link" if !($ARGV[1] eq "move") else $ARGV[1];  # Either move ./.p or link it. ( link is default )

if ($method eq "link") {
    `ln .p
