#!/usr/bin/perl

use open ':locale';

my $broj =  pop(@ARGV);
my %polje;

while (my $red = <>) {
    chomp $red;
    $red = lc($red);
    $red =~ s/[^a-zšđčćž]/ /g;  # zamijenit sve znakove koji nisu hrvatska slova sa razmakom
    my @popis = ($red =~ m/\b(\w{$broj})\b/g);   #pohranit sve rijeci odredene duljine
    foreach my $rijec (@popis) {
        $polje{$rijec} += 1;
    }
}

my @sort = (sort keys %polje);

foreach my $ispis (@sort) {
    print "$ispis : $polje{$ispis}" . "\n";
}