"""
This module contains classes relating to Oxford Nanopore Technologies'
nanopore sequencing.
"""
import re

class Read:
    """Represents a nanopore read.

    Args & Attributes:
        name (str): To identify the read.
        events ([Event]): Ordered list of events that occurred during
            the sequencing of this read.
    """
    def __init__(self, name, contig):
        self.name = name
        self.contig = contig
        self.events = []
        self.is_valid = True

    def add_event(self, event):
        """Adds an event to this Read in chronological order.

        Args:
            event (Event): Event to add to this Read.
        """
        self.events.append(event)

class Event:
    """Represents a k-mer event (when a k-mer temporarily resides in the
    nanopore during nanopore sequencing).

    Args & Attributes:
        position (int): Position of the event with respect to the 
            reference contig that the read has been mapped to.
        ref_kmer (str): Reference k-mer associated with the event.
        samples ([float]): List of current measurements associated with
            the event.
    """
    def __init__(self, position, ref_kmer, samples):
        self.position = position
        self.ref_kmer = ref_kmer
        self.samples = samples

    def add_samples(self, samples):
        """Adds samples to this Event in chronological order.

        Args:
            samples ([float]): List of current measurements to add to
                this event (assuming these samples occurred after the
                samples already held by this Event).
        """
        self.samples.extend(samples)

class Kmer:
    """Represents a k-mer.

    Args & Attributes:
        sequence (str): Nucleotide sequence.
    """
    def __init__(self, sequence):
        self.sequence = sequence

    def is_valid(self):
        """Returns true if this Kmer is valid (contains only the 
        characters A, C, G or T).
        """
        return bool(re.match('^[ACGT]+$', self.sequence))

    def matches(self, other):
        """Returns true if this Kmer has the same sequence has another.

        Args:
            other (Kmer): Kmer to compare to
        """
        return self.sequence == other.sequence

    def is_reverse_complement(self, other):
        """Returns true if this Kmer is the reverse complement of 
        another. E.g. The reverse complement of ACGTA is TACGT

        Args:
            other (Kmer): Kmer to compare to
        """
        if len(self.sequence) != len(other.sequence):
            return False
        reverse_complement = []
        for s in self.sequence[::-1]:
            if s == "A":
                reverse_complement.append("T")
            elif s == "C":
                reverse_complement.append("G")
            elif s == "G":
                reverse_complement.append("C")
            elif s == "T":
                reverse_complement.append("A")
            else:
                return False
        return other.sequence == ("").join(reverse_complement)
