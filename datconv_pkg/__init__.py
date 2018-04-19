# -*- coding: utf-8 -*-
"""
This module provides Datconv class which encapsulate all datconv program features
and can be created and called from other Python script in one of following ways::

    from datconv import Datconv 
    dc = Datconv()
    conf = {...}
    dc.Run(conf)

Or::

    from datconv import Datconv 
    dc = Datconv()
    conf = {...}
    for rec in dc.Iterate(conf):
      print ('Field1: %s' % str(rec['Field1']))
"""

# Standard Python Libs
import sys, traceback
from importlib import import_module
import logging, logging.config

# Libs installed using pip
if __package__ != 'datconv_pkg':
    import yaml

############################################################################
sys.path.append('.')
Logger = None

########################################################################
from .version import *
__author__  = datconv_author
__status__  = datconv_status
__version__ = datconv_version
__date__    = datconv_date

############################################################################
class Datconv:
    """Instead of calling datconv from command line, one can create instance of this class 
    inside other Python script and call its Run() method.
    """
    def __init__(self):
        self._reader_inst = None
        self._filter_inst = None
        self._writer_inst = None
        self._outcon_inst = None
        self._outcon_iter = None
    
    def Run(self, conf):
        """Method that runs conversion process.
        
        :param conf: is a ``dict()`` object with keys as apecified by datconv main YAML configuration file. In this case datconv default configuration file is not used.
        :returns: 2 in case of invalid configuration; 0 if run sucessfully; may throw exception
        """
        try:
            reader_parg = self._Initialize(conf, for_iteration = False)
            if reader_parg is None:
                return 2
            Logger.info('Process: %s', reader_parg)
            self._reader_inst.Process(**reader_parg)
            if hasattr(self._outcon_inst, 'onFinish'):
                self._outcon_inst.onFinish(True)
            Logger.info('Finished SUCESSFULLY') #TODO: Not necessary true, introduce kind of err, warn counters
            return 0

        except KeyboardInterrupt:
            if Logger:
                Logger.info('Process broken on user request (Ctrl-C pressed)')
            else:
                sys.stdout.write('Process broken on user request (Ctrl-C pressed)\n')
            if self._outcon_inst and hasattr(self._outcon_inst, 'onFinish'):
                self._outcon_inst.onFinish(False)
            return 3
        except Exception:
            sys.stderr.write('Exception was thrown during Datconv.Run() execusion\n')
            if Logger:
                sys.stderr.write('Look at configured Logger for more details\n')
                Logger.exception('Exception was thrown during Datconv.Run() execusion')
            else:
                traceback.print_exc()
            if self._outcon_inst and hasattr(self._outcon_inst, 'onFinish'):
                self._outcon_inst.onFinish(False)
            return 1
    
    def Iterate(self, conf):
        """Method that runs conversion process in iteration mode - i.e. every output record is being returned to caling loop.
        
        :param conf: is a ``dict()`` object with keys as apecified by datconv main YAML configuration file. In this case datconv default configuration file is not used.
        """
        try:
            reader_parg = self._Initialize(conf, for_iteration = True)
            if reader_parg is None:
                raise Exception('Invalid datconv configuration')
            Logger.info('Iteration start: %s', reader_parg)
            if self._use_iterator_api():
                Logger.debug('Reader supports iterator interface')
                for obj in self._reader_inst.Iterate(**reader_parg):
                    yield obj
            else:
                assert self._outcon_iter
                Logger.debug('Reader does not support iterator interface, reading to memory and then iterate')
                self._reader_inst.Process(**reader_parg)
                for obj in self._outcon_iter:
                    yield obj
            if hasattr(self._outcon_inst, 'onFinish'):
                self._outcon_inst.onFinish(True)
            Logger.info('Finished SUCESSFULLY') #TODO: Not necessary true, introduce kind of err, warn counters

        except KeyboardInterrupt:
            if Logger:
                Logger.info('Process broken on user request (Ctrl-C pressed)')
            else:
                sys.stdout.write('Process broken on user request (Ctrl-C pressed)\n')
            if self._outcon_inst and hasattr(self._outcon_inst, 'onFinish'):
                self._outcon_inst.onFinish(False)
            raise StopIteration
        except Exception:
            sys.stderr.write('Exception was thrown during Datconv.Run() execusion\n')
            if Logger:
                sys.stderr.write('Look at configured Logger for more details\n')
                Logger.exception('Exception was thrown during Datconv.Run() execusion')
            else:
                traceback.print_exc()
            if self._outcon_inst and hasattr(self._outcon_inst, 'onFinish'):
                self._outcon_inst.onFinish(False)
            raise
    
    def GetHeader(self):
        """Returns Header assiciated with data.
        Method intendent to be used with iteration interface.
        """
        if self._writer_inst:
            return self._writer_inst.getHeader()
        else:
            return None
    
    def GetFooter(self):
        """Returns Footer assiciated with data.
        Method intendent to be used with iteration interface.
        """
        if self._writer_inst:
            return self._writer_inst.getFooter()
        else:
            return None
            
    def Version(self, ext_module = None, ext_verobj = '__version__'):
        """If ext_module is None method returns datconv version.
           Otherwise it loads ext_module module and returns its ext_verobj object (``__version__`` by default).
        """
        if ext_module is None:
            return datconv_version
        try:
            ext_mod = import_module(ext_module)
            ext_ver = getattr(ext_mod, ext_verobj)
            return str(ext_ver)
        except ImportError:
            return 'Not installed'
    
    def _Initialize(self, conf, for_iteration):
        from datconv.outconn import dcstdout, dcfile, dcnull, dccollector, dcmultiplicator
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
        elif isinstance(logger_conf, str):
            Logger = logging.getLogger(logger_conf).getChild(logger_name)
        else:
            logger_lev = conf.get('DefLogLevel')
            if logger_lev == 'CRITICAL':
                llevel = logging.CRITICAL
                lstream = sys.stderr
            elif logger_lev == 'ERROR':
                llevel = logging.ERROR
                lstream = sys.stderr
            elif logger_lev == 'WARNING':
                llevel = logging.WARNING
                lstream = sys.stderr
            elif logger_lev == 'INFO':
                llevel = logging.INFO
                lstream = sys.stdout
            elif logger_lev == 'DEBUG':
                llevel = logging.DEBUG
                lstream = sys.stdout
            else:
                llevel = logging.ERROR
                lstream = sys.stderr
            logging.basicConfig(stream = lstream, level = llevel)
            Logger = logging.getLogger(logger_name)

        ####################################################################
        ## Read configuration
        reader_conf = conf.get('Reader')
        if reader_conf is None:
            Logger.critical('Obligatory "Reader" key not defined in configuration')
            return None
        reader_path = reader_conf.get('Module')
        if reader_path is None:
            Logger.critical('Obligatory "Reader":{"Module"} key not defined in configuration')
            return None
        reader_mod = import_module(reader_path)
        reader_mod.Log = Logger.getChild('reader')
        reader_class = getattr(reader_mod, 'DCReader')
        Logger.debug('Reader: %s(%s)', reader_path, str(reader_conf.get('CArg')))

        writer_conf = conf.get('Writer')
        if writer_conf is None:
            Logger.critical('Obligatory "Writer" key not defined in configuration')
            return None
        writer_path = writer_conf.get('Module')
        if writer_path is None:
            Logger.critical('Obligatory "Writer":{"Module"} key not defined in configuration')
            return None
        writer_mod = import_module(writer_path)
        writer_mod.Log = Logger.getChild('writer')
        writer_class = getattr(writer_mod, 'DCWriter')
        Logger.debug('Writer: %s(%s)', writer_path, str(writer_conf.get('CArg')))

        filter_conf = conf.get('Filter')
        if filter_conf is not None:
            filter_path = filter_conf.get('Module')
            if filter_path is not None:
                filter_mod = import_module(filter_path)
                filter_mod.Log = Logger.getChild('filter')
                filter_class = getattr(filter_mod, 'DCFilter')
                Logger.debug('Filter: %s(%s)', filter_path, str(filter_conf.get('CArg')))
            else:
                filter_class = None
        else:
            filter_class = None

        outcon_conf = conf.get('OutConnector')
        if outcon_conf is not None:
            outcon_path = outcon_conf.get('Module')
            if outcon_path is not None:
                outcon_mod = import_module(outcon_path)
                outcon_mod.Log = Logger.getChild('outcon')
                outcon_class = getattr(outcon_mod, 'DCConnector')
                Logger.debug('OutConnector: %s(%s)', outcon_path, str(outcon_conf.get('CArg')))
            else:
                outcon_class = None
        else:
            outcon_class = None

        ####################################################################
        ## Convert file
        reader_carg = reader_conf.get('CArg')
        self._reader_inst = reader_class(**reader_carg) if reader_carg else reader_class()
        writer_carg = writer_conf.get('CArg')
        self._writer_inst = writer_class(**writer_carg) if writer_carg else writer_class()
        filter_carg = None if filter_conf is None else filter_conf.get('CArg')
        self._filter_inst = None if filter_class is None else (filter_class(**filter_carg) if filter_carg else filter_class())
        outcon_carg = None if outcon_conf is None else outcon_conf.get('CArg')
        self._outcon_inst = None if outcon_class is None else (outcon_class(**outcon_carg) if outcon_carg else outcon_class())
        if self._outcon_inst is None:
            if 'PArg' in reader_conf and 'outpath' in reader_conf['PArg']:
                dcfile.Log = Logger.getChild('outcon')
                self._outcon_inst = dcfile.DCConnector(path = reader_conf['PArg']['outpath'])
                Logger.debug('Fallback output connector: datconv.outconn.dcfile(%s)', reader_conf['PArg']['outpath'])
            elif for_iteration:
                self._outcon_inst = dcnull.DCConnector()
            else:
                self._outcon_inst = dcstdout.DCConnector()
                Logger.debug('Fallback output connector: datconv.outconn.dcstdout')
        else:
            if 'PArg' in reader_conf and 'outpath' in reader_conf['PArg']:
                Logger.warning('Reader:PArg:outpath key will be ignored because there is output connector configured')
        if for_iteration and not self._use_iterator_api():
            dccollector.Log = Logger.getChild('outcon')
            dcmultiplicator.Log = Logger.getChild('outcon')
            self._outcon_iter = dccollector.DCConnector()
            self._outcon_inst = \
                dcmultiplicator.DCConnector(self._outcon_inst, self._outcon_iter)

        self._writer_inst.setOutput(self._outcon_inst)
        self._reader_inst.setWriter(self._writer_inst)
        if self._filter_inst is not None:
            self._reader_inst.setFilter(self._filter_inst)

        reader_parg = reader_conf.get('PArg')
        return reader_parg

    def _use_iterator_api(self):
        import datconv.writers.dcxpaths
        return hasattr(self._reader_inst, 'Iterate') and not \
            isinstance(self._writer_inst, datconv.writers.dcxpaths.DCWriter)
        
########################################################################
### Helpers

def _RemoveCArg(MasterD, MergedD):
    """
    Remove ``CArg:`` key from MergedD when respective ``Module:`` keys does not match.
    """
    assert isinstance(MasterD, dict)
    assert isinstance(MergedD, dict)
    for key in MasterD.keys():
        if key in MergedD:
            if isinstance(MergedD[key], dict) and isinstance(MasterD[key], dict):
                _RemoveCArg(MasterD[key], MergedD[key])
            elif key == 'Module':
                if MergedD[key] != MasterD[key]:
                    if 'CArg' in MergedD:
                        del MergedD['CArg']

def _MergeDict(MasterD, MergedD):
    """
    Requrently adds keys from MergedD to MasterD in the way that MasterD keys are not overwritten.
    """
    assert isinstance(MasterD, dict)
    assert isinstance(MergedD, dict)

    for key in MergedD.keys():
        if key not in MasterD:
            MasterD[key] = MergedD[key]
        else:
            if isinstance(MergedD[key], dict) and isinstance(MasterD[key], dict):
                _MergeDict(MasterD[key], MergedD[key])

def _DatconvMergeConf(MasterD, MergedD):
    _RemoveCArg(MasterD, MergedD)
    _MergeDict(MasterD, MergedD)
