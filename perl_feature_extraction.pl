
use strict;
use warnings;

# Reading the list of files
my $list = "liste_fichiers_part.txt";
open(my $input, "<", $list) or die "Cannot open $list: $!";

while (my $file = <$input>) {
    chomp($file);
    # Remove unnecessary prefixes and postfixes from the file path
    $file =~ s/^alignement_Lucile\///; # Remove 'alignement_Lucile/' from the beginning
    $file =~ s/\/ctm$//; # Remove '/ctm' from the end
    my ($filename) = $file =~ m|.*/([^/]+\.wav)$|; # Extract filename with .wav extension
    print "Processing file: $filename\n"; # Debug print
    if ($filename) {
        # Run Python script to extract features
        system("/usr/bin/python3 feature_extraction.py $file");
    }
}

close($input);

