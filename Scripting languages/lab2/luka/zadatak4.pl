#!/usr/bin/perl

if (scalar(@ARGV != 1)){
    die "Potrebno je navesti datoteku.\n";
}

my $logfile = $ARGV[0];
open(my $fh, "<", $logfile) or die "Ne mogu otvoriti $datoteka !";

my $poglavlje = ""; 
my $potpoglavlje = "";
my $brojac_poglavlja = 0;
my $brojac_potpoglavlja = 0;

while (my $line = <$fh>) {
    chomp $line;
        
    if ($line =~ /<h1>(.+)<\/h1>/) {
        $poglavlje = $1;
        $brojac_poglavlja++;
        print "$brojac_poglavlja. $poglavlje\n";
        $potpoglavlje = "";
        $brojac_potpoglavlja = 0; 
    }

    if ($line =~ /<h2>(.+)<\/h2>/){
        $potpoglavlje = $1;
        $brojac_potpoglavlja++;
        print "               $brojac_poglavlja.$brojac_potpoglavlja. $potpoglavlje\n";
    }

}

close $fh;





