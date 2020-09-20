# EventParser
Software for parsing aligned event files to HDF5 format to improve the ease of downstream analysis of event data generated during Nanopore sequencing.

# Background

## What is Nanopore sequencing?
Nanopore sequencing is a method of DNA or RNA sequencing where a DNA or RNA strand is translocated through a nanopore with electric current flowing through it.  Translocation of DNA or RNA through the pore causes current fluctuations characteristic of the bases (A, C, G, T or U), allowing determination of the base sequence from the electric current signal. For more info see here: https://nanoporetech.com/how-it-works

## What is an event?
At any given time during Nanopore sequencing, the nanopore contains k bases (a "k-mer").  An event is the raw current signal associated with that k-mer.

## What is an aligned event file?
Due to errors in the basecalling process (converting raw signal to base sequence), the calculated events may contain errors.  Several software packages exist that rectify these errors (e.g. Nanopolish eventalign module https://github.com/jts/nanopolish or Tombo resquiggle module https://github.com/nanoporetech/tombo).  Each software package outputs the corrected events and their raw signal assignment in a file that we refer to here as the "aligned event file".  The format of this file is different per software.

## What is EventParser useful for?
Aligned event files can be difficult to query directly (e.g. Nanopolish eventalign files are .tsv format with a varying number of lines per event) without some form of pre-processing for each query.  EventParser can be run once to convert the aligned event file into HDF5 format, which downstream analyses can easily query.  EventParser currently supports Nanopolish eventalign files but can easily be extended to support aligned event files from other software packages.  This would allow aligned events from any software to be converted to the same intermediate data structure, so that downstream event processing can be independent of the software used to align events.

# Installation
```
git clone https://github.com/a-sneddon/eventparser
cd eventparser
pip install -e .
pip install -r scripts/requirements.txt
```

# Usage
```
parse_aligned_events.py [-h] [-o OUTPUT] input_file {eventalign,tombo}

positional arguments:
  input_file            The aligned event file to be parsed
  {eventalign,tombo}    Type of aligned event file.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        dir to write the HDF5 file to.
```

# Demo

## Example input (excerpt of Nanopolish .tsv file)
| contig | position | reference_kmer | read_name | strand | event_index | event_level_mean | event_stdv | event_length | model_kmer | model_mean | model_stdv | standardized_level | start_idx | end_idx | samples |
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
| ENST00000448958.2 | 1405 | AGAAG | c1654154 | t | 5 | 134.01 | 7.72 | 0.00232 | AGAAG | 142.76 | 12.22 | -0.48 | 17484 | 17491 | 124.569,122.055 |
| ENST00000448958.2 | 1405 | AGAAG | c1654154 | t | 6 | 142.6 | 9.225 | 0.0083 | AGAAG | 142.76 | 12.22 | -0.01 | 17459 | 17484 | 123.978,133.59,105.196 |
| ENST00000448958.2 | 1406 | GAAGA | c1654154 | t | 7 | 118.55 | 7.076 | 0.02191 | GAAGA | 125.18 | 8.93 | -0.5 | 17393 | 17459 | 105.049,96.6192,119.097,93.07 |
| ENST00000448958.2 | 1407 | AAGAA | c1654154 | t | 8 | 141.87 | 4.679 | 0.00465 | AAGAA | 141.3 | 12.9 | 0.03 | 17379 | 17393 | 126.64,122.351,123.534,134.773 |
| ENST00000448958.2 | 1407 | AAGAA | c1654154 | t | 9 | 137.88 | 6.98 | 0.00764 | AAGAA | 141.3 | 12.9 | -0.18 | 17356 | 17379 | 125.9,129.301,129.006,123.978,117.914,110.816 |
| ENST00000448958.2 | 1408 | AGAAA | c1654154 | t | 11 | 143.32 | 11.773 | 0.00631 | AGAAA | 147.06 | 12.22 | -0.21 | 17321 | 17340 | 103.422,102.682,128.414,136.991 |
| ENST00000448958.2 | 1408 | AGAAA | c1654154 | t | 12 | 156.18 | 4.811 | 0.00332 | AGAAA | 147.06 | 12.22 | 0.5 | 17311 | 17321 | 142.611,142.167,129.006,133.442,131.076,133.59 |
| ENST00000448958.2 | 1408 | AGAAA | c1654154 | t | 13 | 139.11 | 10.884 | 0.00498 | AGAAA | 147.06 | 12.22 | -0.44 | 17296 | 17311 | 118.654,132.555,123.83,129.154 |
| ENST00000457540.1 | 69 | TCGCA | ae666552 | t | 96 | 91.09 | 3.01 | 0.00498 | TCGCA | 87.62 | 3.62 | 0.81 | 34305 | 34320 | 95.582,91.634,89.581,90.8444 |
| ENST00000457540.1 | 69 | TCGCA | ae666552 | t | 98 | 89.99 | 2.086 | 0.00697 | TCGCA | 87.62 | 3.62 | 0.56 | 34277 | 34298 | 88.0018,91.1602,92.8974,88.7914 |
| ENST00000457540.1 | 69 | TCGCA | ae666552 | t | 99 | 91.33 | 3.335 | 0.00432 | TCGCA | 87.62 | 3.62 | 0.87 | 34264 | 34277 | 89.581,92.7394,83.8958,94.4766,86.5804 |
| ENST00000457540.1 | 70 | CGCAC | ae666552 | t | 100 | 102.49 | 2.191 | 0.00531 | CGCAC | 100.85 | 5.36 | 0.26 | 34248 | 34264 | 100.636,100.32,103.478,99.846,103.32,107.268 |
| ENST00000457540.1 | 70 | CGCAC | ae666552 | t | 101 | 86.49 | 2.596 | 0.00664 | CGCAC | 100.85 | 5.36 | -2.27 | 34228 | 34248 | 84.8433,89.7389,83.422,85.475,83.8958,80.2635,86.4225 |
| ENST00000457540.1 | 71 | GCACT | ae666552 | t | 102 | 82.36 | 1.484 | 0.00465 | GCACT | 78.63 | 2.61 | 1.21 | 34214 | 34228 | 82.1586,80.8952,79.7898,82.6324 |

## Example output (.h5 file structure)
```
read-c1654154
    name: c1654154
    contig: ENST00000448958.2
    events:
        event-1405:
            position: 1405
            ref_kmer: AGAAG
            samples: [124.569,122.055,123.978,133.59,105.196]
        event-1406:
            position: 1406
            ref_kmer: GAAGA
            samples: [105.049,96.6192,119.097,93.07]
        event-1407:
            position: 1407
            ref_kmer: AAGAA
            samples: [126.64,122.351,123.534,134.773,125.9,129.301,129.006,123.978,117.914,110.816]
        event-1408:
            position: 1408
            ref_kmer: AGAAA
            samples: [103.422,102.682,128.414,136.991,142.611,142.167,129.006,133.442,131.076,133.59,118.654,132.555,123.83,129.154]
read-ae666552:
    name: ae666552
    contig: ENST00000457540.1
    events:
        event-69:
            position: 69
            ref_kmer: TCGCA
            samples: [95.582,91.634,89.581,90.8444,88.0018,91.1602,92.8974,88.7914,89.581,92.7394,83.8958,94.4766,86.5804]
        event-70:
            position: 70
            ref_kmer: CGCAC
            samples: [100.636,100.32,103.478,99.846,103.32,107.268,84.8433,89.7389,83.422,85.475,83.8958,80.2635,86.4225]
        event-71:
            position: 71
            ref_kmer: GCACT
            samples: [82.1586,80.8952,79.7898,82.6324]
```

## How to run the demo
```
python3 scripts/parse_aligned_events.py demo/demo_eventalign.tsv eventalign -o demo/
```

# Release Notes
* 1.0 Initial release