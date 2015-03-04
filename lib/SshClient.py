#!/usr/bin/env python

'''
__author__ = 'santhosh'
__Desc__ = SSH Client Library used for establishing an ssh connection
           Runs Commands and retrieve Command Output
__Version__ = 1.0
'''

import paramiko
import time
from ReturnCodes import FAIL, SUCCESS
from config.Config import Cfg


class SshClient(object):
    def __init__(self, host):

        self.host = None
        self.port = 22
        self.user = Cfg['user']
        self.passwd = Cfg['passwd']
        self.keyPairFiles = Cfg['keyPairFiles']
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.retryCnt = 0
        self.delay = 0
        self.timeout = 3.0
        self.host = host
        self.retryCnt = Cfg['retries']
        self.delay = Cfg['delay']
        self.timeout = Cfg['timeout']
        self.port = Cfg['port']


    def __createConnection(self):
        '''
        @Name: createConnection
        @Desc: Creates an ssh connection for
               retries mentioned,along with sleep mentioned
        @Output: SUCCESS on successful connection
                 FAIL If connection through ssh failed
        '''
        ret = FAIL
        while self.retryCnt >= 0:
            try:
                if self.keyPairFiles is None:
                    self.ssh.connect(hostname=self.host,
                                     port=self.port,
                                     username=self.user,
                                     password=self.passwd,
                                     timeout=self.timeout)
                else:
                    self.ssh.connect(hostname=self.host,
                                     port=self.port,
                                     username=self.user,
                                     password=self.passwd,
                                     key_filename=self.keyPairFiles,
                                     timeout=self.timeout,
                                     look_for_keys=False
                                     )
                ret = SUCCESS
                break
            except Exception as se:
                self.retryCnt = self.retryCnt - 1
                if self.retryCnt == 0:
                    break
                time.sleep(self.delay)
        return ret

    def runCommand(self, command):
        '''
        @Name: runCommand
        @Desc: Runs a command over ssh and
               returns the result along with status code
        @Input: command to execute
        @Output: 1: status of command executed.
                 Default to None
                 SUCCESS : If command execution is successful
                 FAIL    : If command execution has failed
                 EXCEPTION_OCCURRED: Exception occurred while executing
                                     command
                 INVALID_INPUT : If invalid value for command is passed
                 2: stdin,stdout,stderr values of command output
        '''
        excep_msg = ''
        ret = {"status": FAIL, "stdin": None, "stdout": None, "stderr": None}
        if command is None or command == '':
            ret["status"] = FAIL
            return ret
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.readlines()
            errors = stderr.readlines()
            inp = stdin.readlines()
            ret["stdin"] = inp
            ret["stdout"] = output
            ret["stderr"] = errors
            if stdout is not None:
                if stdout.channel.recv_exit_status() == 0:
                    ret["status"] = SUCCESS
        except Exception as e:
            excep_msg = str(e)
        finally:
            print " Host: %s Cmd: %s Output:%s Exception: %s" %(self.host, command, str(ret), excep_msg)
            return ret

    def close(self):
            if self.ssh is not None:
                self.ssh.close()


