#!/usr/bin/perl

my %count;
my $date;
my %requests_per_hour;

foreach my $logfile (@ARGV) {
    open(my $fh, "<", $logfile) or die "Can't open $logfile: $!";
        if ($logfile =~ /(\d{4})-(\d{2})-(\d{2})/) {
        my $date = "$3/$2/$1";
        }
        print "Datum: $date\n";
        print "sat : broj pristupa\n";
        print "-------------------------------\n";
        
    while (<$fh>) {
    my ($day, $month, $year, $hour, $minute, $second) = $_ =~ m{^(\d+)/(\w+)/(\d+):(\d+):(\d+):(\d+)};
    my $time = "$year-$month-$day $hour:00:00";
    $requests_per_hour{$time}++;
    }

    close $fh;

    foreach my $time (sort keys %requests_per_hour) {
    printf("%s: %d\n", $time, $requests_per_hour{$time});
    }
   
}
