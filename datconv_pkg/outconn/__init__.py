"""Common data or structures to be used in Datconv Output Connectors."""

STRING  = 0x01
"""Bit meeaning that Connector accepts strings."""

OBJECT = 0x02
"""Bit meeaning that Connector accepts objects."""

LIST  = 0x04
"""Bit meeaning that Connector accepts list objects."""

ITERABLE  = 0x08
"""Bit meeaning that Connector accepts Python iterable objects."""

from datconv.version import *
__author__  = datconv_author
__status__  = datconv_status
__version__ = datconv_version
__date__    = datconv_date
