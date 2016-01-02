"""Common data or structures to be used in Pandoc Filters.

SKIP   - Name for zero, when Filter returnes this value record is skipped.
WRITE  - When Filter returns this bit record is being posted to Writer.
REPEAT - When Filter returns this bit other bits are checked and flow is again returned to Filter function with the same record. This bit is used to generate/produce data.
BREAK  - When Filter returns this bit impot process is breaken and DCWriter.writeFooter function is being called.
"""

SKIP   = 0x00
WRITE  = 0x01
REPEAT = 0x02
BREAK  = 0x04

from datconv.version import *
__author__  = datconv_author
__status__  = datconv_status
__version__ = datconv_version
__date__    = datconv_date
