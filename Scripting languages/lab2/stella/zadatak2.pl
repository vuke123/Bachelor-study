#!/usr/bin/perl

print "Unesite niz brojeva odvojenih razmakom: ";
my @numbers = split(' ', <STDIN>);
chomp @numbers;

my $sum = 0;
$sum += $_ for @numbers;

my $avg = $sum / @numbers;
print "Aritmeticka sredina: $avg\n";