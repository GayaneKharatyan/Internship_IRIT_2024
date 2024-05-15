#!/usr/bin/perl
use strict;
use warnings;

# Reading the list of files
my $list = "liste_fichiers.txt";
open(my $input, "<", $list) or die "Cannot open $list: $!";

while (my $file = <$input>) {
    chomp($file);
    # Extracting file path without extension
    my ($filename) = $file =~ m|alignement_Lucile/([^/]+/[^/]+\.wav)/ctm$|;
    # Run Python script to split the WAV file
    system("/usr/bin/python3 cut.py \"$filename\"");
}

close($input);

