# -*- coding: utf-8 -*-
"""This module contain skeleton class suitable as starting point for new Datconv output connectors."""

# Standard Python Libs
import logging

# Datconv generic modules
from . import STRING, OBJECT, LIST, ITERABLE

####################################################################
Log = None
"""Log varaible is automatically set by main pandoc script using logging.getLogger method.
Use it for logging messages in need.
"""

class DCConnector:
    """This class must be named exactly DCConnector.
    It is being called by Writter in order to write output data.
    It's main task is to:
    
    - write data to destination storage (which can be file, database, some stream)
    """
    def __init__(self):
        """Additional constructor parameters may be added to this method, but they all have to be named parameters.
        Parameters are usually passed from YAML file as subkeys of OutConnector:CArg key.
        """
        assert Log is not None
        # ...

    def supportedInterfases(self):
        """Obligatory method that must be defined in Output Connector class.
        Informs Writer about kind of interface this connector implements.
        Connector should return one or combination of flags: STRING, OBJECT, LIST, ITERABLE.
        If is called by Writer before it pass any data to connector.
        """
        return STRING

    def pushString(self, strData):
        """Obligatory method that must be defined if Connector returned STRING flag in supportedInterfases() method.
        It is called by Writer to pass data to be written to output.
        Connector must write passed data to output.
        Method does not return any value.
        
        :param strData: string to be written to output.
        """
        pass

    def getStreams(self):
        """Obligatory method that must be defined if Connector returned STRING flag in supportedInterfases() method.
        It may be called by Writer to obtain output stream to write to (instead of calling pushString.
        It may happen if Writer uses some library functions that require stream to be passed to.
        Connector must return array of its output streams (must be a list - typically one element).
        
        :return: list of streams for writing data.
        """
        return []
    
    def tryObject(self, obj):
        """Obligatory method that must be defined if Connector returned OBJECT flag in supportedInterfases() method.
        It is called by Writer before it pass any data to connector (but after supportedInterfases)
        to check if it is configured with compatible connector.
        Passed object is of the same type like it will be later passed to pushObject() method.
        Connector should call isinstance() and return True if object is of right type.
        
        :param obj: object passed for hands shaking.
        :return: boolean value indicating if passed object is of correct type.
        """
        return True

    def pushObject(self, obj):
        """Obligatory method that must be defined if Connector returned OBJECT flag in supportedInterfases() method.
        It is called by Writer to pass data to be written to output.
        Connector must write passed data to output.
        Method does not return any value.
        
        :param obj: object to be written to output.
        """
        pass

    def onFinish(self, bSuccess):
        """Optional method that may be defined.
        If it is defined it is called by Writer at and of conversion process.
        Connector may use it to close its streams, commit data or just log proper message.
        Method does not return any value.
        
        :param bSuccess: parameter that inform connector if process is going to end sucessfully.
        """
        if bSuccess:
            print ('Output sucessfully written to XXX')
        else:
            print ('There was error, output written to XXX is invalid')
