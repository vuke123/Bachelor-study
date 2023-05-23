#!/usr/bin/perl


my $input_file = shift @ARGV;

open my $fh, '<', $input_file or die "Can't open $input_file: $!";
my $bvze = <$fh>;
my $factors_line = <$fh>;
chomp $factors_line;
my @factors = split /;/, $factors_line;

while (my $line = <$fh>) {
    chomp $line;
    next if $line =~ /^\s*$/ or $line =~ /^\s*#/;
   
    my ($jmbag, $surname, $name, @scores) = split /;/, $line;
    next if $surname =~ /\d/;
    my $total = 0;
    for (my $i = 0; $i < scalar @scores; $i++) {
        next if $scores[$i] eq '-';
        $total += $scores[$i] * $factors[$i];
    }

    printf "%s, %s (%s) : %.2f\n", $surname, $name, $jmbag, $total;
}

close $fh;
