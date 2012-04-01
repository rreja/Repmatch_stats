use strict;
use warnings;
use Getopt::Std;

my %opt;
getopt('ki',\%opt);

&help_message if (defined $opt{h});

# Ask the user to input the file directory which contains the key.txt, orphan.txt and summary.txt files
my $keypath = $opt{'k'};;
#Ask the user to input the directory which contains the S_* files.
my $pp_path = $opt{'i'};;

open IN, $keypath."key.txt" || die "key.txt file not found. Please check your path has '/' at the end";
open IN3, $keypath."orphan.txt" || die "orphan.txt file not found. Please check your path has '/' at the end";
open OUT, ">".$keypath."output_repmatch_stats.tab" || die "Output file not found";

print OUT "id\tFilename\t#peak-pair\t#peak-pair_in_replicate\t%_top1%tile_peak-pairs-in-replicate\t%_top5%tile_peak-pairs-in-replicate\t";
print OUT "%_top10%tile_peak-pairs-in-replicate\t%_top25%tile_peak-pairs-in-replicate\t%_top50%tile_peak-pairs-in-replicate\t";
print OUT "%_top75%tile_peak-pairs-in-replicate\t%_top100%tile_peak-pairs-in-replicate\n";

# Reading the orphan.txt file to see how many peaks were not found in more than 2 replicates.
my %orphan = ();

while(<IN3>){
    chomp($_);
    next if($_ =~ /^chrom/);
    my @cols = split(/\t/,$_);
    $orphan{$cols[0]."_".$cols[1]."_".$cols[2]."_".$cols[4]} = $cols[5];
    #$orphan{$cols[0]."_".$cols[1]."_".$cols[2]} = $cols[5];
    
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
        next if($_ =~ /^#/);
        $_ =~ s/^M//g;
        my @vals = split(/\t/,$_);
        my @cwdist = split(/=/,$vals[8]);
        $peak_pairs{$vals[0]."_".$vals[3]."_".$vals[4]."_".$cwdist[1]} = $vals[5];
        #$peak_pairs{$vals[0]."_".$vals[3]."_".$vals[4]} = $vals[5];
    
    }
    
    
    my ($quant_1_not_orphan,$pp1) = find_quantile(\%peak_pairs,1,$id);
    my ($quant_5_not_orphan,$pp5) = find_quantile(\%peak_pairs,5,$id);
    my ($quant_10_not_orphan,$pp10) = find_quantile(\%peak_pairs,10,$id);
    my ($quant_25_not_orphan,$pp25) = find_quantile(\%peak_pairs,25,$id);
    my ($quant_50_not_orphan,$pp50) = find_quantile(\%peak_pairs,50,$id);
    my ($quant_75_not_orphan,$pp75) = find_quantile(\%peak_pairs,75,$id);
    my ($quant_100_not_orphan,$pp100) = find_quantile(\%peak_pairs,100,$id);
    print OUT $id."\t".$fname."\t".scalar(keys %peak_pairs)."\t".$pp100."\t".$quant_1_not_orphan."\t";
    print OUT $quant_5_not_orphan."\t".$quant_10_not_orphan."\t".$quant_25_not_orphan."\t".$quant_50_not_orphan."\t";
    print OUT $quant_75_not_orphan."\t".$quant_100_not_orphan."\n";
    close(IN1);
        
}

sub find_quantile{
    my($hash,$cutoff,$id) = @_;
    my $length = scalar(keys %$hash);
    my $quant = int($length*($cutoff/100));
    my $count = 0;
    my $found_in_orphan = 0;
    foreach my $key (sort { $$hash {$b} <=> $$hash {$a}} keys %$hash )
    {
        last if($count == $quant);
        #print $key."\t".$$hash{$key}."\n";
        
        if(exists($orphan{$key}) && ($orphan{$key} == $id)){
            $found_in_orphan++;
            
        }
        $count++;
    }
    
    my $pp_in_replicate = $quant - $found_in_orphan;
    return (($pp_in_replicate/$quant), $pp_in_replicate);
}





sub help_message {
  print qq{
    Program: repmatch_stats.pl (Calculate stats on rep match output files)
    Contact: Rohit Reja <rzr142\@psu.edu>
    Usage:   repmatch_stats.pl -k <path_to_key.txt_file> -i <path_to_S_*_files>

    Options: -k <path1>     path to the folder with key.txt and orphan.txt file. Path should end with a '/' 
             -i <path2>     path to the folder with S_*.gff files. Path should end with a '/' 
             -h             help

    Example:
      perl repmatch_stats.pl -k  /usr/local/folder/ -i /folder1/peakpairs/
      
    Output:
    Produces a "output_repmatch_stats.tab" file in the folder that contains the  key.txt and orphan.txt files.
  
  };
  exit;
}
