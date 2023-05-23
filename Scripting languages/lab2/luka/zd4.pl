#!/usr/bin/perl

my $input_file = shift @ARGV;

open my $fh, '<', $input_file or die "Can't open $input_file: $!";

while (my $line = <$fh>) {

    chomp $line;

    my ($jmbag, $surname, $name, $termin, $zakljucano) = split /;/, $line;

    my ($termin_date, $termin_time1, $termin_time2, $classroom) = split / /, $termin;
    my ($zakljucano_date, $zakljucano_time) = split / /, $zakljucano;

    my $termin_seconds1 = &to_seconds($termin_time1);
    my $termin_seconds2 = &to_seconds($termin_time2);

    my $zakljucano_seconds = &to_seconds($zakljucano_time);

    if ($zakljucano_seconds < $termin_seconds1 || $zakljucano_seconds > $termin_seconds2) {
        print "$jmbag $surname $name - PROBLEM $termin_date $termin_time --> $zakljucano\n";
    }
}

close $fh;

sub to_seconds {
    my ($time) = @_;

    my ($hours, $minutes, $seconds) = split /:/, $time;

    return $hours * 3600 + $minutes * 60 + $seconds;
}
