import pytest
from eventparser.factory import AlignedEventParserFactory, AlignedEventType
from eventparser.parser import AlignedEventParser
from eventparser.eventalign import EventalignReadParser, TomboReadParser

def test_create_with_eventalign_event_type():
    factory = AlignedEventParserFactory()
    parser = factory.create(AlignedEventType.NANOPOLISH_EVENTALIGN)
    assert isinstance(parser, AlignedEventParser)
    assert isinstance(parser.read_parser, EventalignReadParser)

def test_create_with_tombo_event_type():
    factory = AlignedEventParserFactory()
    parser = factory.create(AlignedEventType.TOMBO_FAST5)
    assert isinstance(parser, AlignedEventParser)
    assert isinstance(parser.read_parser, TomboReadParser)

def test_create_with_invalid_event_type():
    factory = AlignedEventParserFactory()
    with pytest.raises(ValueError):
        factory.create("invalid_event_type")
