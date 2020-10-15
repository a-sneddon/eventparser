import pytest
from eventparser.ont import Read, Event, Kmer

def test_read_add_event_with_event():
    read = Read("read123", "ENST0")
    assert len(read.events) == 0
    event = Event(1, "ACGT", 1, 3)
    read.add_event(event)
    assert len(read.events) == 1

# def test_event_add_samples_with_samples():
#     event = Event(1, "ACGT", 1, 3)
#     event.add_samples([0.3, 0.4])
#     assert event.samples == [0.1, 0.2, 0.3, 0.4]

def test_kmer_is_valid_with_valid_sequence():
    kmer = Kmer("ACGTTTCCCCGACAAAATCG")
    assert kmer.is_valid() == True

def test_kmer_is_valid_with_invalid_first_char():
    kmer = Kmer("FACGC")
    assert kmer.is_valid() == False

def test_kmer_is_valid_with_invalid_middle_char():
    kmer = Kmer("TAGDC")
    assert kmer.is_valid() == False

def test_kmer_is_valid_with_invalid_last_char():
    kmer = Kmer("ACTCN")
    assert kmer.is_valid() == False

def test_kmer_matches_with_same_kmer():
    kmer = Kmer("ACGTCCCCA")
    other_kmer = Kmer("ACGTCCCCA")
    assert kmer.matches(other_kmer) == True

def test_kmer_matches_with_different_kmer():
    kmer = Kmer("ACGTC")
    other_kmer = Kmer("AAGTC")
    assert kmer.matches(other_kmer) == False

def test_kmer_is_reverse_complement_with_reverse_complement_kmer():
    kmer = Kmer("ACGTC")
    other_kmer = Kmer("GACGT")
    assert kmer.is_reverse_complement(other_kmer) == True
    assert other_kmer.is_reverse_complement(kmer) == True

def test_kmer_is_reverse_complement_with_non_reverse_complement_kmer():
    kmer = Kmer("ACGTCA")
    other_kmer = Kmer("TGACGG")
    assert kmer.is_reverse_complement(other_kmer) == False

def test_kmer_is_reverse_complement_with_invalid_kmer():
    kmer = Kmer("ACGTCA")
    other_kmer = Kmer("ACGTCAN")
    assert kmer.is_reverse_complement(other_kmer) == False