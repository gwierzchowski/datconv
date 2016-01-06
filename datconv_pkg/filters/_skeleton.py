# -*- coding: utf-8 -*-
# Checked with python 2.7
"""This module contain Datconv Filter skeleton class suitable as starting point for new filters."""

# Standard Python Libs
import logging

# Libs installed using pip
from lxml import etree

# Datconv generic modules
from datconv.filters import SKIP, WRITE, REPEAT, BREAK

####################################################################
Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCFilter:
    """This class must be called exactly DCFilter.
    It is being called after Reader read record and before Writer wrote record.
    It is able to:
      - filter data (i.e. do not pass certain records further - i.e. to writer for placing in output)
      - change data (i.e. change on the fly contents of certain records)
      - produce data (i.e. cause that certain records, maybe slightly modified, are being sent multiply times to writer)
      - break conversion process (i.e. caused that conversion stop on certain record).
    """
    def __init__(self):
        """Method called when object is being created.
        Additional parameters may be added to this method, but they all have to be named parameters.
        Parameters are usually passed from YAML file as subkeys of Filter:CArg key.
        """
        assert Log is not None
        # ...

    def filterRecord(self, record):
        """Obligatory method that must be defined in Filter class.
        It is called to perform filter tasks described above.
        record - is instance of root XML model of record returned by Reader (class of lxml.etree.ElementTree).
        This method may check or manipulate contents of record.
        
        Most frequently used methods:
        record.tag - the name of root tag (i.e. record name).
        record.find(xpath) - returns first found (or None) record sub-tag using relative, simplified xpath.
           e.g. record.find('.//TIME') - searches record tree and returns first found <TIME .../> tag.
        record.findtext(xpath) - as above but returns .text attribute (see below) of found tag (or raise Exception if tag is not found)..
        record.xpath(xpath) - evaluate full absolute xpath extression on record (i.e. return list of matched tags, or string, number etc. - depands on xpath).
           e.g. record.xpath('/Gampdf_winNbrs/winSet') - returns list of all winSet subtags of root Gampdf_winNbrs tag.
        On record and also on tags returned by above methods the data associated with tag may be obtained using:
        tag.tag - tag name (i.e. field name)
        tag.text - text that is contained between opening and closing tag (usually data value)
        tag.keys() - iterable containing tag attbibute names
        tag['attrib'] - the value of tag attribute named 'attrib'; raise Exception if tag does not contain 'attrib' atribute.
        tag.get('attrib') - as above but returns None if no such attribute.
        record.insert(0, newtag) - inserts new tag at begining of record
        etree.SubElement(record, 'NEWTAG') - inserts new tag at and of record
        See lxml package for more documentation.
        
        This method should return combination of following bits:
        WRITE  - to cause program to pass record to Writer for writting to output
        REPEAT - to cause program to call filterRecord with the same record (instead or reading next record from input).
                 This is used to produce / create new records.
                 This option should be used with caution to avoid infinite loop (i.e. Filter should mainain its own replication maximal count).
        BREAK  - to cause program to break process on this record (i.e. Reader will not read next record).
                 In case when REPEAT | BREAK is returned, the REPEAT bit takes precedence.
        or return SKIP (0) - what will cause that record will be skiped (will not be passed to Writer).
        """
        return WRITE

    