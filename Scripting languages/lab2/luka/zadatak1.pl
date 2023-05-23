#!/usr/bin/perl

print "Unesite niz znakova: ";
my $niz = <STDIN>;
chomp $niz;

print "Unesite broj ponavljanja: ";
my $n = <STDIN>;
chomp $n;

for (my $i = 0; $i < $n; $i++) {
    print "$niz\n";
}
