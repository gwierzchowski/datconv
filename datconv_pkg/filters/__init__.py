"""Common data or structures to be used in Datconv Filters."""

SKIP   = 0x00
"""Name for zero, when Filter returnes this value record is skipped."""

WRITE  = 0x01
"""When Filter returns this bit, record is being posted to Writer."""

REPEAT = 0x02
"""When Filter returns this bit, other bits are checked and flow is again returned to Filter function 
with the same record. This bit is used to generate/produce data."""

BREAK  = 0x04
"""When Filter returns this bit, impot process is breaken and DCWriter.writeFooter function is being called."""

from datconv.version import *
__author__  = datconv_author
__status__  = datconv_status
__version__ = datconv_version
__date__    = datconv_date
