#!/usr/bin/perl

my $input_file = shift @ARGV;

open my $fh, '<', $input_file or die "Ne mogu otvoriti $input_file: $!";

<$fh>;

my $factors_line = <$fh>;
chomp $factors_line;
my @factors = split /;/, $factors_line;

while (my $line = <$fh>) {
    chomp $line;
    next if $line =~ /^\s*#/;

    my ($jmbag, $surname, $name, @scores) = split /;/, $line;
    
    my $total = 0;
    foreach my $i (@scores) {
        next if $scores[$i] eq '-';
        $total += $scores[$i] * $factors[$i];
    }

    printf "%s, %s (%s) : %.2f\n", $surname, $name, $jmbag, $total;
}

close $fh;
