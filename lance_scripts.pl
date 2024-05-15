#!/usr/bin/perl



my $list = "liste_fichiers.txt";
open (L, "<$list") or die $!;
while (<L>) {
    chomp;
    $fichier=$_;
    #$rec=$fichier.".wav.burst";
    #$power="alignement_pataka/".$fichier.".pwr.pwr.pwr";
    #print $rec."\n";
    
    system ("python ctm2stat.py $fichier >> G_result_voice4PD.txt ");
    
}



