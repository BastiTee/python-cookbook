"""Enumeration like data structure."""

def enum(*sequential, **named):
    """Definition for an enumeration like data structure."""
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
