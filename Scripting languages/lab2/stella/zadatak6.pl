#!/usr/bin/perl
use open ':locale';
#export LC_ALL=hr_HR.UTF-8


$number = pop(@ARGV);

while (my $line = <>) {
    chomp $line;
    $line = lc $line;
    my @words = ($line =~ m/\b(\w{$number})\b/g);

    for my $word (@words) {
        $word_count{$word}++;
    }
}

my @sorted_words = sort keys %word_count;
for my $word (@sorted_words) {
    my $count = $word_count{$word};
    print "$word: $count\n";
}
