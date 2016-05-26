# -*- coding: utf-8 -*-
"""
This module provides Datconv class which encapsulate all datconv features
and can be created and called from other Python script as e.g.:

import datconv
...
    pd = Datconv()
    conf = ...
    pd.Run(conf)
"""

# Standard Python Libs
import sys
from importlib import import_module
import logging, logging.config

# Libs installed using pip
if __package__ != 'datconv_pkg':
    import yaml


############################################################################
sys.path.append('.')
Logger = None

############################################################################
class Datconv:
    """Instead of calling datconv from command line, one can create this class instance
    inside other Python script and call its Run() method.
    """
    def Run(self, conf):
        """Method that runs conversion peocess.
        conf - is a dict() object with keys as apecified by datconv main YAML configuration file.
        Returns: 2 in case of invalid configuration; 0 if run sucessfully; may throw exception
        """
        ####################################################################
        ## Set-up Logger
        global Logger
        logger_name = 'datconv'
        logger_conf = conf.get('Logger')
        if isinstance(logger_conf, dict):
            if logger_conf.get('Conf'):
                logger_conf = yaml.load(open(logger_conf.get('Conf')).read())
            logging.config.dictConfig(logger_conf)
            Logger = logging.getLogger(logger_name)
        if isinstance(logger_conf, str):
            Logger = logging.getLogger(logger_conf).getChild(logger_name)
        else:
            logging.basicConfig(stream = sys.stderr, level = logging.WARNING)
            Logger = logging.getLogger(logger_name)

        ####################################################################
        ## Read configuration
        reader_conf = conf.get('Reader')
        if reader_conf is None:
            Logger.critical('Obligatory "Reader" key not defined in configuration')
            return 2
        reader_path = reader_conf.get('Module')
        if reader_path is None:
            Logger.critical('Obligatory "Reader":{"Module"} key not defined in configuration')
            return 2
        reader_mod = import_module(reader_path)
        # reader_mod.Log = logging.getLogger(logger_name + '.reader')
        reader_mod.Log = Logger.getChild('reader')
        reader_class = getattr(reader_mod, 'DCReader')
        Logger.debug('Reader: %s(%s)', reader_class, reader_conf.get('CArg'))

        writer_conf = conf.get('Writer')
        if writer_conf is None:
            Logger.critical('Obligatory "Writer" key not defined in configuration')
            return 2
        writer_path = writer_conf.get('Module')
        if writer_path is None:
            Logger.critical('Obligatory "Writer":{"Module"} key not defined in configuration')
            return 2
        writer_mod = import_module(writer_path)
        # writer_mod.Log = logging.getLogger(logger_name + '.writer')
        writer_mod.Log = Logger.getChild('writer')
        writer_class = getattr(writer_mod, 'DCWriter')
        Logger.debug('Writer: %s(%s)', writer_class, writer_conf.get('CArg'))

        filter_conf = conf.get('Filter')
        if filter_conf is not None:
            filter_path = filter_conf.get('Module')
            if filter_path is not None:
                filter_mod = import_module(filter_path)
                # filter_mod.Log = logging.getLogger(logger_name + '.filter')
                filter_mod.Log = Logger.getChild('filter')
                filter_class = getattr(filter_mod, 'DCFilter')
                Logger.debug('Filter: %s(%s)', filter_class, filter_conf.get('CArg'))
            else:
                filter_class = None
        else:
            filter_class = None

        ####################################################################
        ## Convert file
        reader_carg = reader_conf.get('CArg')
        reader = reader_class(**reader_carg) if reader_carg else reader_class()
        writer_carg = writer_conf.get('CArg')
        writer = writer_class(**writer_carg) if writer_carg else writer_class()
        filter_carg = None if filter_conf is None else filter_conf.get('CArg')
        filter = None if filter_class is None else (filter_class(**filter_carg) if filter_carg else filter_class())

        reader.setWriter(writer)
        if filter is not None:
            reader.setFilter(filter)

        reader_parg = reader_conf.get('PArg')
        Logger.info('Process: %s', reader_parg)
        reader.Process(**reader_parg)
        Logger.info('Finished SUCESSFULLY') #TODO: Not necessary true, introduce kind of err, warn counters
        return 0


########################################################################
from .version import *
__author__  = datconv_author
__status__  = datconv_status
__version__ = datconv_version
__date__    = datconv_date
