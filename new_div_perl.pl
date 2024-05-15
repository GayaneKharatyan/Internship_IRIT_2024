#!/usr/bin/perl

use strict;
use warnings;

my $list = "textgrid_files.txt";
open (my $input, "<", $list) or die "Cannot open $list: $!";
open (my $output, ">", "G_result_new_division.csv") or die "Cannot open output file: $!";

# Printing the header to CSV file
print $output "File,Part,Start,Average Silence Duration,Speech Rate,Average Vowel Duration,Type\n";

while (my $file = <$input>) {
    chomp($file);
    print "Processing file: $file\n";

    my ($filename, $part) = $file =~ /([^\/]+\.wav)\/([^\/]+)\.(?:TextGrid|textgrid)$/i; # Extracting file name without path and extension
    
    if (!defined $filename || !defined $part) {
        print "Error: Could not extract filename and part from: $file\n";
        next;
    }
    
    # Determine the type based on the filename
    my $type = ($file =~ /ctm\.textgrid$/i) ? 'auto' : 'manuel';

    my $output_content = `python3 new_division.py "$file"`;
    
    my %metrics;
    my %start_times;
    foreach my $line (split(/\n/, $output_content)) {
        if ($line =~ /Metrics for part (\d+):/) {
            $part = $1;
        } elsif ($line =~ /Start: (\d+\.\d+)/) {
            $start_times{$part} = $1;
        } elsif ($line =~ /Average Silence Duration: (\d+\.\d+)/) {
            $metrics{$part}{'Average Silence Duration'} = $1;
        } elsif ($line =~ /Speech Rate: (\d+\.\d+)/) {
            $metrics{$part}{'Speech Rate'} = $1;
        } elsif ($line =~ /Average Vowel Duration: (\d+\.\d+)/) {
            $metrics{$part}{'Average Vowel Duration'} = $1;
        }
    }
    
    foreach my $part (sort {$a <=> $b} keys %metrics) {
        print $output "$filename,$part,$start_times{$part},$metrics{$part}{'Average Silence Duration'},$metrics{$part}{'Speech Rate'},$metrics{$part}{'Average Vowel Duration'},$type\n";
    }
}

close($input);
close($output);

