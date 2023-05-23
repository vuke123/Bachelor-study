#!/usr/bin/perl

print "Unesite niz brojeva odvojenih razmakom: ";
my $input = <STDIN>;
chomp $input;

my @numbers = split(/\s+/, $input);

my $sum = 0;
foreach my $num (@numbers) {
    $sum += $num;
}

my $avg = $sum / scalar(@numbers);
print "Aritmeticka sredina: $avg\n";