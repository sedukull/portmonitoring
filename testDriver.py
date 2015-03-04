'''
__Desc__: Driver Program to run and test IP Port Monitoring tool
          EX: python testDriver.py  '10.10.10.10' 80 25
'''

import argparse
from src.IpPortMonitor import PortMonitor
import threading
import sys
import os
from lib.ReturnCodes import FAIL

if "__name__" != "__main__":
    # Parser to parse the input ip and port arguments
    parser = argparse.ArgumentParser(
        description='IP and Port Monitor. EX Usage: "python testDriver.py -ip 10.10.10.10 -p 25 80"')
    parser.add_argument('-ip', action='store', dest='ip_address',
                        help='IP Address to scan', default=None)
    parser.add_argument('-p', action='store', dest='port_list',
                        help='List of ports separated by single space char EX: 80 25', default=None, nargs='*')
    args = parser.parse_args()
    if (not args.ip_address) or (not args.port_list):
        print "\n=== Invalid Input Arguments, Please Check ==="
        print os.system("python testDriver.py -h")
        sys.exit()
    else:
        port_monitor_obj = PortMonitor()
        try:
            if (port_monitor_obj.parseArgs(args.ip_address, args.port_list) != FAIL):
                print "\n== Launching the Port Monitor Thread ===="  
                t1 = threading.Thread(target=port_monitor_obj.startServices())
                t1.start()
                t1.join()
        except Exception, ex:
            print "=== Exception Occurred. Please Check %s ===" % (ex)
