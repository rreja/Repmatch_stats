Peak Statistics
================

Introduction
-------------

The scriptis in this repository can be used to perform some basic statistics
on the "peak calls". The "peak calls" file is the output file obtained by running
genetrack program on the index/raw tag file.

The basic operations include seperating the singleton and non-singelton peaks and
then calculating the median and average of tag counts and standard deviations.


Requirements
------------

- The software requires only Perl_ (5 or higher) to run.
- The input file should be in standard Gff_ format

Installation
------------

Unpack the source code archive. The folder contains the followng

- `peak_statistics.pl`: Script for basic statistics when running on a single file
- `peak_statistics_batch.sh` : Script for batch processing
- `README.rst` : Readme file
- `sample.gff`: The sample input file to test the scripts.

When running the script on a single input gff file:

- Open the file `peak_statistics.pl` in  any text editor of your choice.
- Comment out the line 18 by putting a "#" in front of it.
- Uncomment the lines 21 and 22 by removing the "#" in front of them.
- You are ready to use the file. How to run the script from your terminal?

- Type the following:

    $ perl  peak_statistics.pl  <path_to_your_input_file>
    $ #for example: peak_statistics.pl /Users/input/sample.gff

An output file with  '_NoS.gff' at the end will be generated, that will
contain all the non-singelton peaks into it (The peaks whose standard deviation
is greater than 0). Also, some statistic summary about the file would be displayed
on the screen. Each column (in the order of display)  contains the following:
    - Filename
    - Percentage of mapped reads
    - Percentage of uniquely mapped reads
    - Total non-singelton peaks
    - Total singelton peaks
    - Median of tag counts for non-singleton peaks
    - Mean of tag counts for non-singleton peaks
    - Median fuzziness (standard deviation) for non-singleton peaks
    - Mean fuzziness (standard deviation) for non-singleton peaks

When batch processing:

- For batch processing DO NOT modify 'peak_statistics.pl' file
- To run the batch script:

    $./peak_statistics_batch.sh # will give the instruction on how to run the file
    $./peak_statistics_batch.sh -i <path_to_directory>
    $ # for example: ./peak_statistics_batch.sh  /Users/input/

Remember, when giving the path to the directory containing files, always give the
path with "/" at the end. For ex: "/Users/input/" is acceptable but "/Users/input"
would generate error.


The batch script would create a foler "output" in the directory containing your
input files. The output folder will contain a "_NoS.gff" file for each input
gff file and a "peak_statistics.txt" file containing the basic statistics for
all the input files present in the directory. "peak_statistics.txt" has the
same format as mentioned above.


.. _Perl: http://www.perl.org/
.. _Gff: http://genome.ucsc.edu/FAQ/FAQformat#format3
~                                                                                                                                                                                                                                                                             

