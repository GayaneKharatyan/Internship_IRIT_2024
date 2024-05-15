#!/usr/bin/perl

use strict;
use warnings;

my $list = "liste_fichiers.txt";
open (my $input, "<", $list) or die "Cannot open $list: $!";
open (my $output, ">", "G_result_voice4PD.csv") or die "Cannot open output file: $!";

#Printing the header to CSV file
print $output "File,Part,Average Silence Duration,Speech Rate,Average Vowel Duration\n";

while (my $file = <$input>) {
    chomp($file);
    my ($filename) = $file =~ m|.*/([^/]+)\.wav/ctm$|; #Extracting file name without path and extension
    
    my $output_content = `python3 ctm2stat.py "$file"`;
    
    my $part = 1;
    my %metrics;
    foreach my $line (split(/\n/, $output_content)) {
        if ($line =~ /Metrics for part (\d+):/) {
            $part = $1;
        } elsif ($line =~ /Average Silence Duration: (\d+\.\d+)/) {
            $metrics{$part}{'Average Silence Duration'} = $1;
        } elsif ($line =~ /Speech Rate: (\d+\.\d+)/) {
            $metrics{$part}{'Speech Rate'} = $1;
        } elsif ($line =~ /Average Vowel Duration: (\d+\.\d+)/) {
            $metrics{$part}{'Average Vowel Duration'} = $1;
        }
    }
    
    foreach my $part (sort keys %metrics) {
        print $output "$filename,$part,$metrics{$part}{'Average Silence Duration'},$metrics{$part}{'Speech Rate'},$metrics{$part}{'Average Vowel Duration'}\n";
    }
}

close($input);
close($output);

