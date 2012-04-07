Replicate-match Statistics
================

Introduction
-------------

The scripts in this repository can be used to perform some basic statistics on the replicate-match files. The replicate-match files are the output file obtained by running rep-match python script on the peak-pair file.

The basic operations include counting a) peak-pairs in replicates and increasing window quantile scan of peak-pairs in replicates.

Requirements
------------

- The script only requires Perl_ (5 or higher) to run.


THE SCRIPT WILL BREAK IF:
------------------------

- The files have excel ^M character in it. For sanity check, open your file in terminal, to see if you can see ^M character in your file. In case, you find ^M character in your file, use the following command to remove it::

    $ perl -p -e 's/^M/\n/g;' <file_with_excel_char> > <new_file>

- If you change the name of the files "key.txt" and "orphan.txt", that are present in the folder produced by the repmatch script. 


Installing and Running the scripts
------------

Unpack the source code archive. The folder contains the following::

-  repmatch_stats.pl: Script for basic statistics. 
-  README.rst: Readme file
-  Sample data: which includes (three peak-pair files: S_Reb1-rep2_s5e10F1_stdev.gff, S_Reb1-rep3_s5e10F1stdev.gff, S_Reb1-rep4_s5e10F1stdev.gff and a folder (repmatch_output_closest_d50r2u37l17) containing the output of repmatch script, that contains the primary files "key.txt" and "orphan.txt" used by the script.


If you get more information on option then type this::

    $ perl  repmatch_stats.pl -h

Do a test run of the script by typing::

$ perl repmatch_stats.pl -k  /usr/local/folder -i /folder1/peakpairs

The folder should now contain a "repmatch_stats.txt" file. This means that script runs fine on your system.



Output
------

All output files will be produced in the folder that contain "key.txt" and "orphan.txt" files.
Following output files will be generated:


- "repmatch_stats.txt" containing the summary for each input file. The summary includes the following information::

    - Filename
    - number of Peak-pair 
    - number of peak-pair in relicates. 
    - top_1pt_peak-pairs_in_replicates.
    - top_5pt_peak-pairs_in_replicates. 
    - top_10pt_peak-pairs_in_replicates.
    - top_25pt_peak-pairs_in_replicates.
    - top_50pt_peak-pairs_in_replicates.
    - top_75pt_peak-pairs_in_replicates.
    - top_100pt_peak-pairs_in_replicates.
  
   

.. _Perl: http://www.perl.org/
.. _Gff: http://genome.ucsc.edu/FAQ/FAQformat#format3
