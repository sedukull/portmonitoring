'''
__author__ = 'Santhosh'
__Desc__  = Module for providing logging facilities to IP Port Scanner
'''

from config.Config import Cfg
import sys
import time
import os
import logging
from ReturnCodes import SUCCESS, FAIL
import random


class ScanLogger(object):

    '''
    @Name  : ScanLog
    @Desc  : provides interface for logging to scanner
    @Input : logger_name : name for logger
    '''
    logFormat = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    _instance = None
    LoggerName = "ip_port_scan"

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ScanLogger, cls).__new__(cls, cls.LoggerName)
            return cls._instance

    def __init__(self):
        '''
        @Name: __init__
        @Input: logger_name for logger
        '''

        '''
        Logger for Logging Info
        '''
        self.__logger = None
        self.__logFilePath = None

    def __setLogHandler(self):
        '''
        @Name : __setLogHandler
        @Desc: Adds the given Log handler to the current logger
        @Output: SUCCESS if no issues else FAIL
        '''
        try:
            self.__logger = logging.getLogger(self.LoggerName)
            self.__logger.setLevel(logging.DEBUG)
            temp_ts = time.strftime("%b_%d_%Y_%H_%M_%S",
                                    time.localtime())
            temp_path = Cfg['log_file_path'] + "//" + \
                str(temp_ts) + "_" + str(random.random())
            os.makedirs(temp_path)
            self.__logFilePath = temp_path + "/runinfo.txt"
            print "===Log File Path :%s ==="%str(self.__logFilePath)
            file_stream = logging.FileHandler(self.__logFilePath)
            file_stream.setFormatter(self.logFormat)
            file_stream.setLevel(logging.DEBUG)
            self.__logger.addHandler(file_stream)
            # Now add handler to print to stdout
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(self.logFormat)
            stream_handler.setLevel(logging.DEBUG)
            self.__logger.addHandler(stream_handler)
            return SUCCESS
        except Exception as e:
            print "\nException Occurred Under " \
                  "__setLogHandler %s" % e
            return FAIL

    def getLogger(self):
        '''
        @Name : createLogs
        @Desc : Gets the Logger with file paths initialized and created
        @Inputs :creating log folder path
        @Output : SUCCESS\FAIL
        '''
        try:
            self.__setLogHandler()
            return self.__logger
        except Exception as e:
            raise "\n Exception Occurred While creating Logger :%s" % \
                e
