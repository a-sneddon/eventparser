import csv
import json
import pytest
from eventparser.eventalign import EventalignReadParser

IN="tests/integration/data/eventalign/"
OUT="tests/integration/data/json/"

"""
Test fixtures
"""
def load_expected_data(json_file):
    with open(json_file) as f:
        reads = json.load(f)
    return reads

@pytest.fixture
def single_read_test_file():
    test_file = open('{0}single_read.tsv'.format(IN))
    yield test_file
    test_file.close()

@pytest.fixture
def single_read_expected():
    return load_expected_data('{0}single_read.json'.format(OUT))

@pytest.fixture
def multiple_read_test_file():
    test_file = open('{0}multiple_reads.tsv'.format(IN))
    yield test_file
    test_file.close()

@pytest.fixture
def multiple_read_expected():
    return load_expected_data('{0}multiple_reads.json'.format(OUT))

@pytest.fixture
def repeated_position_test_file():
    test_file = open('{0}repeated_position.tsv'.format(IN))
    yield test_file
    test_file.close()

@pytest.fixture
def repeated_position_expected():
    return load_expected_data('{0}repeated_position.json'.format(OUT))

@pytest.fixture
def skipped_position_test_file():
    test_file = open('{0}skipped_position.tsv'.format(IN))
    yield test_file
    test_file.close()

@pytest.fixture
def skipped_position_expected():
    return load_expected_data('{0}skipped_position.json'.format(OUT))

@pytest.fixture
def model_kmer_NNNNN_test_file():
    test_file = open('{0}model_kmer_NNNNN.tsv'.format(IN))
    yield test_file
    test_file.close()

@pytest.fixture
def model_kmer_NNNNN_expected():
    return load_expected_data('{0}model_kmer_NNNNN.json'.format(OUT))

@pytest.fixture
def repeated_kmer_test_file():
    test_file = open('{0}repeated_kmer.tsv'.format(IN))
    yield test_file
    test_file.close()

@pytest.fixture
def repeated_kmer_expected():
    return load_expected_data('{0}repeated_kmer.json'.format(OUT))

def is_event_correct(actual_event, expected_json):
    print(actual_event.samples)
    print(expected_json["samples"])

    return actual_event.position == expected_json["position"] and \
        actual_event.ref_kmer.sequence == expected_json["ref_kmer"] and \
        actual_event.samples == expected_json["samples"]

"""
Test EventAlign file that contains events for a single read.

E.g.:
contig	position	reference_kmer	read_name	...	
ENST00000448958.2	1406	GAAGA	read_123 ...	
ENST00000448958.2	1407	AAGAA	read_123 ...
ENST00000448958.2	1408	AGAAA	read_123 ...

In this case, the output should be a single Read object for read_123.
"""
def test_parse_reads_with_single_read_file_returns_one_read(
    single_read_test_file):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(single_read_test_file))
    assert len(reads) == 1

def test_parse_reads_with_single_read_file_returns_correct_name(
    single_read_test_file, single_read_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(single_read_test_file))
    assert reads[0].name == single_read_expected["name"]

def test_parse_reads_with_single_read_file_returns_correct_contig(
    single_read_test_file, single_read_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(single_read_test_file))
    assert reads[0].contig == single_read_expected["contig"]

def test_parse_reads_with_single_read_file_returns_correct_events(
    single_read_test_file, single_read_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(single_read_test_file))
    for i, event in enumerate(reads[0].events):
        expected_event = single_read_expected["events"][i]
        assert is_event_correct(event, expected_event) == True

"""
Test EventAlign file that contains events for multiple reads.

E.g.:
contig	position	reference_kmer	read_name	...	
ENST00000448958.2	1406	GAAGA	read_123 ...	
ENST00000448958.2	1407	AAGAA	read_123 ...
ENST00000448958.2	1408	AGAAA	read_123 ...
ENST00000551111.2	1302	AGAAA	read_124 ...
ENST00000551111.2	1303	GAAAA	read_124 ...
ENST00000551111.2	1304	AAAAC	read_124 ...

In this case, the output should be both reads.
"""
def test_parse_reads_with_multiple_read_file_returns_multiple_reads(
    multiple_read_test_file, multiple_read_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(multiple_read_test_file))
    assert len(reads) == len(multiple_read_expected)

def test_parse_reads_with_multiple_read_file_returns_correct_names(
    multiple_read_test_file, multiple_read_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(multiple_read_test_file))
    for i, read in enumerate(reads):
        assert read.name == multiple_read_expected[i]["name"]

def test_parse_reads_with_multiple_read_file_returns_correct_contigs(
    multiple_read_test_file, multiple_read_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(multiple_read_test_file))
    for i, read in enumerate(reads):
        assert read.contig == multiple_read_expected[i]["contig"]

def test_parse_reads_with_multiple_read_file_returns_correct_events(
    multiple_read_test_file, multiple_read_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(multiple_read_test_file))
    for i, _ in enumerate(reads):
        for j, event in enumerate(reads[i].events):
            expected_event = multiple_read_expected[i]["events"][j]
            assert is_event_correct(event, expected_event) == True

"""
Test EventAlign file that contains a repeated position.

E.g.:
contig	position	reference_kmer	read_name	...	
ENST00000448958.2	1406	GAAGA	read_123 ...	
ENST00000448958.2	1407	AAGAA	read_123 ...
ENST00000448958.2	1408	AGAAA	read_123 ...
ENST00000448958.2	1408	AGAAA	read_123 ...
ENST00000448958.2	1408	AGAAA	read_123 ...
ENST00000448958.2	1408	AGAAA	read_123 ...
ENST00000448958.2	1409	GAAAA	read_123 ...
ENST00000448958.2	1410	AAAAC	read_123 ...

In this case, position 1408 is repeated because the k-mer AGAAA took a 
long time to translocate through the pore and the event was segmented 
too many times.  The output list of events should only contain the event
for k-mer AGAAA (position 1408) once, and the signal for that event
should have all the samples for that k-mer concatenated in order.
"""
def test_parse_reads_with_repeated_position_returns_one_event(
    repeated_position_test_file, repeated_position_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(repeated_position_test_file))
    for i, event in enumerate(reads[0].events):
        expected_event = repeated_position_expected["events"][i]
        assert is_event_correct(event, expected_event) == True

"""
Test EventAlign file that contains a skipped position.

E.g.:
contig	position	reference_kmer	read_name	...	
ENST00000448958.2	1406	GAAGA	read_123 ...	
ENST00000448958.2	1407	AAGAA	read_123 ...
ENST00000448958.2	1409	GAAAA	read_123 ...
ENST00000448958.2	1410	AAAAC	read_123 ...

In this case, position 1408 is missing.  read_123 should still be 
parsed and the output should also have no event at position 1408.
"""
def test_parse_reads_with_skipped_position_returns_correct_events(
    skipped_position_test_file, skipped_position_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(skipped_position_test_file))
    for i, _ in enumerate(reads):
        for j, event in enumerate(reads[i].events):
            expected_event = skipped_position_expected[i]["events"][j]
            assert is_event_correct(event, expected_event) == True

"""
Test EventAlign file that contains an event where the model_kmer is
'NNNNN', which is denoted by nanopolish to mean an event caused by
sequencing artifact that needs to be skipped.

E.g.:
contig	position	reference_kmer	... model_kmer
ENST00000448958.2	1406	GAAGA	... TCTTC	
ENST00000448958.2	1407	AAGAA	... NNNNN
ENST00000448958.2	1408	GAAAA	... TTTTC
ENST00000448958.2	1409	AAAAC	... GTTTT

In this case, the event 1407 should be skipped.
"""
def test_parse_reads_with_model_kmer_NNNNN_returns_correct_events(
    model_kmer_NNNNN_test_file, model_kmer_NNNNN_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(model_kmer_NNNNN_test_file))
    for i, _ in enumerate(reads):
        for j, event in enumerate(reads[i].events):
            expected_event = model_kmer_NNNNN_expected[i]["events"][j]
            assert is_event_correct(event, expected_event) == True

"""
Test EventAlign file that contains two consecutive events that have the
same k-mer, but are at different positions.

E.g.:
contig	position	reference_kmer	... model_kmer
ENST00000448958.2	1406	AAAAA	... AAAAA	
ENST00000448958.2	1407	AAAAA	... AAAAA
ENST00000448958.2	1408	AAAAC	... AAAAC
ENST00000448958.2	1409	AAACG	... AAACG

In this case, the output should have two separate events for position
1406 and 1407, even though they have the same k-mer.
"""
def test_parse_reads_with_repeated_kmer_returns_separate_events(
    repeated_kmer_test_file, repeated_kmer_expected):
    parser = EventalignReadParser()
    reads = list(parser.parse_reads(repeated_kmer_test_file))
    for i, event in enumerate(reads[0].events):
        expected_event = repeated_kmer_expected["events"][i]
        assert is_event_correct(event, expected_event) == True
