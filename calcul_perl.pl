#!/usr/bin/perl

use strict;
use warnings;

my $list = "liste_fichiers.txt";
open (my $input, "<", $list) or die "Cannot open $list: $!";
open (my $output, ">", "Comp_calcul_G_result_voice4PD.csv") or die "Cannot open output file: $!";

# Printing the header to CSV file
print $output "File,Average Silence Duration,Speech Rate,Average Vowel Duration\n";

while (my $file = <$input>) {
    chomp($file);
    my ($filename) = $file =~ m|.*/([^/]+)\.wav/ctm$|; # Extracting file name without path and extension
    
    my $output_content = `python3 calcul.py "$file"`;
    
    my %metrics;
    foreach my $line (split(/\n/, $output_content)) {
        if ($line =~ /Metrics for the entire data:/) {
            next; # Skip this line
        } elsif ($line =~ /Average Silence Duration: (\d+\.\d+)/) {
            $metrics{'Average Silence Duration'} = $1;
        } elsif ($line =~ /Speech Rate: (\d+\.\d+)/) {
            $metrics{'Speech Rate'} = $1;
        } elsif ($line =~ /Average Vowel Duration: (\d+\.\d+)/) {
            $metrics{'Average Vowel Duration'} = $1;
        }
    }
    
    print $output "$filename,$metrics{'Average Silence Duration'},$metrics{'Speech Rate'},$metrics{'Average Vowel Duration'}\n";
}

close($input);
close($output);

