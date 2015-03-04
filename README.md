# portmonitoring
A simple python based tool to verify a given ip address is reachable or not and check given ports are opened or closed. If closed, start the services

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

           EX Usage: python testDriver.py -ip 10.10.10.10 -p 25 80
__Version__ = 1.0
__Input__ =  Cmd Line Arguments are IpAddress and Port List
'''
