import pytest
from eventparser.eventalign import Line

def test_is_valid_with_valid_data():
    line = Line("ENST0", 123, "read_A", "GCACT", "GCACT", [0.1, 0.2])
    assert line.is_valid() == True

def test_is_valid_with_zero_position():
    line = Line("ENST0", 0, "read_A", "GCACT", "GCACT", [0.1, 0.2])
    assert line.is_valid() == True

def test_is_valid_with_invalid_position():
    line = Line("ENST0", -1, "read_A", "GCACT", "GCACT", [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_invalid_ref_kmer():
    line = Line("ENST0", 123, "read_A", "ACNTC", "GCACT", [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_invalid_model_kmer():
    line = Line("ENST0", 123, "read_A", "GCACT", "GCACTYY", [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_mismatching_ref_model_kmers():
    line = Line("ENST0", 123, "read_A", "GCACT", "GCACC", [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_reverse_complement_model_kmer():
    line = Line("ENST0", 123, "read_A", "GCACT", "AGTGC", [0.1, 0.2])
    assert line.is_valid() == True