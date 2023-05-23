#!/usr/bin/perl

my $filename = shift @ARGV;

open my $filehandle, '<', $filename or die "Can't open $filename: $!";

while (my $line = <$filehandle>) {

    chomp $line;

    my ($jmbag, $surname, $name, $start_time, $end_time) = split /;/, $line;

    my ($start_date, $start_time) = split / /, $start_time;
    my ($end_date, $end_time) = split / /, $end_time;

    my $start_timestamp = calculate_timestamp($start_time);
    my $end_timestamp = calculate_timestamp($end_time);

    my $time_difference = $end_timestamp - $start_timestamp;

    if ($time_difference > 3600 || $start_date ne $end_date) {
        print "$jmbag $surname $name - PROBLEM $start_date $start_time --> $end_time\n";
    }
}

close $filehandle;

sub calculate_timestamp {
    my ($time) = @_;

    my ($hours, $minutes, $seconds) = split /:/, $time;

    return $hours * 3600 + $minutes * 60 + $seconds;
}
