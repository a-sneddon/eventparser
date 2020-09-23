import h5py
import os
import pytest
from eventparser.eventalign import EventalignReadParser
from eventparser.parser import AlignedEventParser

IN="tests/integration/data/eventalign/"
OUT="tests/integration/data/h5/"

def test_parse_writes_h5_file_with_correct_path():
    parser = AlignedEventParser(EventalignReadParser())
    parser.parse("{0}model_kmer_NNNNN.tsv".format(IN), OUT)
    assert os.path.isfile('{0}model_kmer_NNNNN.h5'.format(OUT)) == True

def test_parse_raises_exception_if_file_not_found():
    parser = AlignedEventParser(EventalignReadParser())
    with pytest.raises(FileNotFoundError):
        parser.parse("{0}fake_file.tsv".format(IN), OUT)

def test_parse_writes_reads_to_h5_file():
    parser = AlignedEventParser(EventalignReadParser())
    parser.parse("{0}multiple_reads.tsv".format(IN), OUT)
    expected_reads = {"read-c1654154-560c-42e4-a8c1-197e9ade83fb",
        "read-8c329395-b3c6-41f2-82a8-b2b78b4c19de",
        "read-fb90c5fa-859e-455a-87d4-cac02fa565e7"}
    actual_reads = set()
    with h5py.File("{0}multiple_reads.h5".format(OUT), "r") as h5:
        for read in h5.keys():
            actual_reads.add(read)
    assert expected_reads == actual_reads

