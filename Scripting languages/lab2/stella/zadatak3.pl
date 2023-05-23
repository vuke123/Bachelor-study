#!/usr/bin/perl


my %requests_per_hour;

foreach my $logfile (@ARGV) {
    open(my $fh, "<", $logfile) or die "Can't open $logfile: $!";
    my ($date) = $logfile =~ /(\d{4})-(\d{2})-(\d{2})/;
    print "Date: $date\n";
    print "Hour: Requests\n";
    print "------------------------\n";
    while (my $line = <$fh>) {
        my ($day, $month, $year, $hour) = $line =~ /^(\d+)\/(\w+)\/(\d+):(\d+):/;
        my $time = "$year-$month-$day $hour:00:00";
        $requests_per_hour{$time}++;
    }
    close $fh;
    foreach my $time (sort keys %requests_per_hour) {
        printf("%s: %d\n", $time, $requests_per_hour{$time});
    }
    %requests_per_hour = (); 
}