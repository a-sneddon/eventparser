"""
This module contains classes relating to the creation of an 
AlignedEventParser. Since each type of event alignment software
generates a different file type, a different internal parser is used
for each file type.
"""
from enum import Enum
from .eventalign import EventalignReadParser, TomboReadParser
from .parser import AlignedEventParser

class AlignedEventType(Enum):
    """There are currently two tools that generate aligned event files,
    each of which have their own file type:
        1) Nanopolish (https://github.com/jts/nanopolish/)
        2) Tombo (https://github.com/nanoporetech/tombo/)
    """
    NANOPOLISH_EVENTALIGN = 1
    TOMBO_FAST5 = 2

class AlignedEventParserFactory:
    """Responsible for creating an AlignedEventParser with the correct 
    type of ReadParser, which depends on the aligned event file type.

    Args:
        event_type (AlignedEventType): Aligned event file type.
    
    Returns:
        AlignedEventParser
    """
    def create(self, event_type):
        if event_type == AlignedEventType.NANOPOLISH_EVENTALIGN:
            return AlignedEventParser(EventalignReadParser())
        elif event_type == AlignedEventType.TOMBO_FAST5:
            return AlignedEventParser(TomboReadParser())
        else:
            raise ValueError(event_type)