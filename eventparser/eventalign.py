"""
This module contains classes relating to Nanopolish eventalign files.
"""
import csv
import h5py
import re
from abc import ABC, abstractmethod
from .ont import Read, Event, Kmer
from .parser import IReadParser

class EventalignReadParser(IReadParser):
    """Parses an eventalign file read by read.
    """
    def parse_reads(self, in_file):
        """Yields each read in an eventalign file object.
        
        Note: In an eventalign file, a single event may be split across 
        multiple rows (where each row has the same k-mer and position) 
        because of an error in the event segmentation algorithm.  In 
        this case, the data from all rows containing the event must be 
        combined, preserving the order of current measurements.

        Arguments:
            in_file (file object): Eventalign file object to parse.
        """
        reader = csv.reader(in_file, delimiter="\t")
        next(reader) # header
        line = self.__parse_line(next(reader))
        read = Read(line.read_name, line.contig)
        event = Event(line.position, line.ref_kmer, line.samples)
        for line in reader:
            line = self.__parse_line(line)
            if line.is_valid() == False:
                continue
            if line.read_name == read.name:
                if line.position == event.position:
                    event.add_samples(line.samples)
                elif line.position == event.position + 1:
                    read.add_event(event)
                    event = Event(line.position, line.ref_kmer, line.samples)
                else:
                    read.is_valid = False
            else:
                read.add_event(event)
                yield read
                read = Read(line.read_name, line.contig)
                event = Event(line.position, line.ref_kmer, line.samples)
        read.add_event(event)
        yield read

    def __parse_line(self, line):
        """Parses one line in an eventalign file.

        Args:
            line ([]): Tab-separated line in an eventalign file.

        Returns:
            Line
        """
        contig = line[0]
        position = int(line[1])
        read_name = line[3]
        ref_kmer = line[2]
        model_kmer = line[9]
        samples = [float(x) for x in line[15].split(',')]
        return Line(contig, position, read_name, ref_kmer, model_kmer, samples)

class Line:
    """Represents one line in a Nanopolish eventalign file.
    
    Args & Attributes:
        contig (str): Reference contig.
        position (int): Position of the reference k-mer with respect to 
            the reference contig.
        read_name (str): Name of the nanopore read.
        ref_kmer (str): Reference k-mer.
        model_kmer (str): Model k-mer.
        samples ([float]): List of current measurements.
    """
    def __init__(self, contig, position, read_name, ref_kmer, model_kmer, samples):
        self.contig = contig
        self.position = position
        self.read_name = read_name
        self.ref_kmer = Kmer(ref_kmer)
        self.model_kmer = Kmer(model_kmer)
        self.samples = samples

    def is_valid(self):
        """Determines whether this line's data is valid.  There are
        restrictions on the values that position, ref_kmer and 
        model_kmer can take.

        Returns:
            bool: Whether or not the line is valid.
        """
        valid_position = self.position >= 0
        valid_kmers = self.__are_kmers_valid()
        return valid_position and valid_kmers

    def __are_kmers_valid(self):
        valid_ref_kmer = self.ref_kmer.is_valid()
        valid_model_kmer = self.model_kmer.is_valid()
        match = self.ref_kmer.matches(self.model_kmer)
        reverse_complement = self.ref_kmer.is_reverse_complement(self.model_kmer)
        return valid_ref_kmer and valid_model_kmer and (match or reverse_complement)

class TomboReadParser(IReadParser):
    def parse_reads(self, stream):
        # TODO
        pass