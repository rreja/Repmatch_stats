use strict;
use warnings;

# Ask the user to input the file directory which contains the key.txt, orphan.txt and summary.txt files
my $keypath = $ARGV[0];
#Ask the user to input the directory which contains the S_* files.
my $pp_path = $ARGV[1];

open IN, $ARGV[0]."key.txt" || die "key.txt file not found. Please check your path has '/' at the end";
open IN3, $ARGV[0]."orphan.txt" || die "orphan.txt file not found. Please check your path has '/' at the end";

# Reading the orphan.txt file to see how many peaks were not found in more than 2 replicates.
my %replicate = ();

while(<IN3>){
    chomp($_);
    next if($_ =~ /^chrom/);
    my @cols = split(/\t/,$_);
    $replicate{$cols[0]."_".$cols[1]."_".$cols[2]} = $cols[5];
    
}

# reading the key.txt to find out how many replicates exists and then read them individually.
while(<IN>){
    chomp($_);
    next if($_ =~ /^id/);
    my @cols = split(/\t/,$_);
    my $id = $cols[0];
    my @files = split(/\//,$cols[1]);
    my $fname = pop(@files);
    # reading each peak-pair file here.
    open IN1, $pp_path.$fname || die $fname." not found. Please check your path has '/' at the end";
    my %peak_pairs = ();
    while(<IN1>){
        chomp($_);
        my @vals = split(/\t/,$_);
        $peak_pairs{$vals[0]."_".$vals[3]."_".$vals[4]} = $vals[5];
        
    }
#    foreach my $a (@sorted_tags){
#        print $a."\n";
#    }
#    exit;
    close(IN1);
    
}

