r"""This module contains an enumeration like data structure and various
enumerations used in other modules."""

def enum(*sequential, **named):
    """Definition for an enumeration like data structure."""
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
