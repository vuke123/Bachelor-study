#!/usr/bin/perl

print "Unesite niz znakova: ";
chomp(my $niz = <STDIN>);

print "Unesite broj ponavljanja: ";
chomp(my $n = <STDIN>);

print "$niz\n" x $n;
