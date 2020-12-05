"""
Public namedtuples 
"""

from collections import namedtuple

# pointer to occurence of node in source-file
Terminator = namedtuple("Terminator", "client date linenumber payload")

# used in app.py
QuerySyntax = namedtuple("QuerySyntax", "StartEnd Find Between Client Sort")

# used in Query.StartEnd
IntervalPair = namedtuple("IntervalPair", "delta pointer_A pointer_B")
