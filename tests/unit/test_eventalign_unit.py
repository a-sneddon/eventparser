import pytest
from eventparser.eventalign import Line

def test_is_valid_with_valid_data():
    line = Line("ENST0", 123, "read_A", "GCACT", "GCACT", 1, 3, [0.1, 0.2])
    assert line.is_valid() == True

def test_is_valid_with_zero_position():
    line = Line("ENST0", 0, "read_A", "GCACT", "GCACT", 1, 3, [0.1, 0.2])
    assert line.is_valid() == True

def test_is_valid_with_invalid_position():
    line = Line("ENST0", -1, "read_A", "GCACT", "GCACT", 1, 3, [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_invalid_ref_kmer():
    line = Line("ENST0", 123, "read_A", "ACNTC", "GCACT", 1, 3, [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_invalid_model_kmer():
    line = Line("ENST0", 123, "read_A", "GCACT", "GCACTYY", 1, 3, [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_mismatching_ref_model_kmers():
    line = Line("ENST0", 123, "read_A", "GCACT", "GCACC", 1, 3, [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_reverse_complement_model_kmer():
    line = Line("ENST0", 123, "read_A", "GCACT", "AGTGC", 1, 3, [0.1, 0.2])
    assert line.is_valid() == True

def test_is_valid_with_end_after_start_index():
    line = Line("ENST0", 123, "read_A", "GCACT", "AGTGC", 10, 11, [0.1, 0.2])
    assert line.is_valid() == True

def test_is_valid_with_end_before_start_index():
    line = Line("ENST0", 123, "read_A", "GCACT", "AGTGC", 4, 3, [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_end_and_start_index_same():
    line = Line("ENST0", 123, "read_A", "GCACT", "AGTGC", 4, 4, [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_start_index_negative():
    line = Line("ENST0", 123, "read_A", "GCACT", "AGTGC", -1, 4, [0.1, 0.2])
    assert line.is_valid() == False

def test_is_valid_with_start_index_zero():
    line = Line("ENST0", 123, "read_A", "GCACT", "AGTGC", 0, 4, [0.1, 0.2])
    assert line.is_valid() == True

def test_is_valid_with_end_index_negative():
    line = Line("ENST0", 123, "read_A", "GCACT", "AGTGC", -10, -9, [0.1, 0.2])
    assert line.is_valid() == False
