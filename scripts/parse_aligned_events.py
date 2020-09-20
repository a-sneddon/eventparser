"""
This script is used for parsing an aligned event file to HDF5 format.

The aligned event file can be created using either Nanopolish's 
eventalign module, or Tombo.

This script should be invoked as follows:

usage: parse_aligned_events.py [-h] [-o OUTPUT] input_file {eventalign,tombo}

positional arguments:
  input_file            The aligned event file to be parsed
  {eventalign,tombo}    Type of aligned event file.

optional arguments:
  -h, --help            show this help message and exit
  -o, --output          dir to write the HDF5 file to.
"""
import argparse
import sys
from eventparser.factory import AlignedEventParserFactory, AlignedEventType

def check_format(in_file):
    file_format = in_file.split(".")[-1]
    if file_format != "tsv":
        raise argparse.ArgumentTypeError("Input file must be .tsv!")
    return in_file

def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Parses an aligned event file to HDF5 format.")
    parser.add_argument("input_file",
                        type=check_format,
                        help="The aligned event file to be parsed")
    parser.add_argument("file_type",
                        choices=["eventalign", "tombo"],
                        help="Type of aligned event file.")
    parser.add_argument("-o", "--output",
                        default="",
                        help="dir to write the HDF5 file to.")
    return parser.parse_args()

def parse_file(in_file, file_type, out_dir):
    if file_type == "eventalign":
        event_type = AlignedEventType.NANOPOLISH_EVENTALIGN
    elif file_type == "tombo":
        # event_type = AlignedEventType.TOMBO_FAST5
        print("Tombo file parsing not yet implemented!")
        return
    else:
        raise ValueError(file_type)
    factory = AlignedEventParserFactory()
    parser = factory.create(event_type)
    parser.parse(in_file, out_dir)

def main():
    args = parse_args(sys.argv[1:])
    parse_file(args.input_file, args.file_type, args.output)

if __name__ == "__main__":
    main()
