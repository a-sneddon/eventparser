"""
This module contains classes relating to parsing aligned event files, 
generated by any software, to allow downstream event processing.
"""
import csv
import h5py
from abc import ABC, abstractmethod

class IReadParser(ABC):
    """Interface to be implemented by classes that parse reads from
    aligned event files.
    """
    @abstractmethod
    def parse_reads(self):
        pass

class AlignedEventParser:
    """For parsing aligned event files into HDF5 format.  Regardless
    of the software used to align events, the output HDF5 format should
    be consistent.

    Args & Attributes:
        read_parser (IReadParser): Used by this Parser for parsing reads
            in the aligned event file.
    """
    def __init__(self, read_parser):
        self.read_parser = read_parser

    def parse(self, filepath, output_dir):
        """Parses an aligned event file and writes it to HDF5 format.

        Args:
            filepath (str): Name of the aligned event file.
            output_dir (str): Directory to write the HDF5 file to.
        """
        h5_filename = filepath.split("/")[-1].split(".")[0] + ".h5"
        h5_filepath = output_dir + "/" + h5_filename
        with open(filepath) as in_file:
            with h5py.File(h5_filepath, "w") as out_file:
                for read in self.read_parser.parse_reads(in_file):
                    self.__write_read_to_h5(read, out_file)

    def __write_read_to_h5(self, read, h5file):
        """Writes a Read object to an HDF5 file.

        Args:
            read (Read): Read to be written to file
            h5file (file object): HDF5 file to write to
        """
        read_group = h5file.create_group("read-{0}".format(read.name), track_order=True)
        read_group.attrs["name"] = read.name
        read_group.attrs["contig"] = read.contig
        for event in read.events:
            event_group = read_group.create_group("event-{0}".format(event.position))
            event_group.attrs["position"] = event.position
            event_group.attrs["ref_kmer"] = event.ref_kmer.sequence
            event_group.attrs["start_idx"] = event.start_idx
            event_group.attrs["end_idx"] = event.end_idx
            # event_group.create_dataset("samples", data = event.samples)
