#!/usr/bin/env python

'''
__author__ = 'santhosh'
__Desc__ = IP and Port Monitor.
           1. Purpose of this IP Port Monitor is to identify and restart the 
              services on closed ports
           2. Supports both IPV4 and IPV6
           3. It works by verifying, whether provided IP is reachable or not.
           4. If IP is reachable, verify mentioned ports are opened or not.
           5. Restart the services which are stopped on those ports.
           6. Uses the SSH service to connect to remote machine and start\stop the services.
           7. Runs multiple Port monitor jobs in parallel
           
           ==== Source Code Info ===
           1. All Configuration information EX: username, password to connect to a remote machine,
           used by the monitoring tool is mentioned under "config/Config.py" file
           2. Ports, Service Names and Default Paths are mentioned under "config/port_services.csv" file
__Version__ = 1.0
__Input__ =  Cmd Line Arguments are IpAddress and Port List
'''



import socket
from lib.SshClient import SshClient
from lib.ReturnCodes import SUCCESS, FAIL
from lib.ScanLog import ScanLogger
from config.Config import Cfg


class PortMonitor(object):
    def __init__(self):
        self.__services = {}
        self.__ip_address = None
        self.__port_list = []
        self.__IPV6 = False
        self.__IPV4 = False
        self.__log_module = ScanLogger().getLogger()
        self.__closed_port_lst = []


    def parseArgs(self, ip_address, port_list):
        try:
            temp_port_list = port_list
            self.__ip_address = ip_address
            if (not self.__ip_address) or (not temp_port_list):
                self.__log_module.info("Invalid Input Arguments. Please Check")
                return FAIL

            #Check 1. Verify whether given address is a valid ipv6\ipv4 address or not
            try:
                socket.inet_pton(socket.AF_INET6, self.__ip_address)
            except socket.error:
                self.__log_module.info("=== Input IP is not an IPV6 Address, will verify for IPV4 ===")
            try:
                socket.inet_pton(socket.AF_INET, self.__ip_address)
            except socket.error:
                self.__log_module.info("=== Input IP is not a valid IPV4 Address ===")
                return FAIL

            #Check 2: Verify valid port ranges
            for port in temp_port_list:
                try:
                    if not int(port) and port not in range(0, 65535):
                        return FAIL
                    #verify whether duplicate ports are entered
                    if port not in self.__port_list:
                        self.__port_list.append(port)
                except Exception, e:
                    self.__log_module.info("===Invalid Port Values===")
                    return FAIL
            self.__log_module.info("=== Parsing Input IP :%s and Port List:%s  Successful ==="%(str(self.__ip_address),str(self.__port_list)))
            return SUCCESS
        except Exception,e:
            self.__log_module.info("=== Parsing Input Arguments Failed, Please Check: \n%s ===" % str(e))
            return FAIL


    def __verifyPortStatus(self):
        try:
            for port in self.__port_list:
                if self.__IPV6:
                    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                    result = sock.connect((self.__ip_address, int(port)))
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect((self.__ip_address, int(port)))
                if result == 0:
                    print "=== Port {}: \t Open ===".format(port)
                else:
                    self.__closed_port_lst.append(port)
                sock.close()
            return SUCCESS 
        except socket.error, e:
            self.__log_module.info("===========Couldn't connect to IP server: %s"
                                  "=========:\nException Trace:%s" % (str(self.__ip_address),str(e)))
            return FAIL
        except Exception, ex:
            self.__log_module.info("===== __verifyPortStatus: Exception Occurred : \n%s=====" %str(ex))
            return FAIL

    def __retrieveServicePaths(self):
        if not self.__closed_port_lst:
            #Read the port Service information
            temp = {}
            for lines in open(Cfg['port_service_info_file_path'],'r').readlines():
                if not lines.startswith('#') and lines != '':
                    line = lines.split(';')
                    temp[line[0]] = line[2]
            for ports in self.__closed_port_lst:
                self.__services[ports] = temp[ports]


    def startServices(self):
        #Retrieve all Service Paths from CSV file
        self.__retrieveServicePaths()
        self.__log_module.info("==Step1: Retrieving Default Port Service Info Successful ===")
        #Verify Port Status for the input provided ports information
        if self.__verifyPortStatus() != SUCCESS:
        	self.__log_module.info("==Step2: Retrieving Closed Port Status Info Failed ===")
                return 
        self.__log_module.info("==Step2: Retrieving Closed Port Status Info Successful ===")
        for port, service_paths in self.__services.items():
            ssh_client = SshClient(self.__ip_address)
            service_paths = service_paths.split(',')
            for items in service_paths:
                ret = ssh_client.runCommand('service ' + items + ' restart')
                if ret['status'] == SUCCESS:
                    self.__log_module.info("\nService %s Started Successfully" % items)
                    break
                else:
                    self.__log_module.info("\nService %s Start Failed" % items)
        return 

