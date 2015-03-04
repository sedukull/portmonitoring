'''
__author__ = 'santhosh'
__Desc__ = Provides the Config Information for the port monitoring
'''

Cfg = {
   'user' : 'root',
   'passwd' : 'password',
   'retries' : 20,
   'delay' : 30,
   'timeout' : 10.0,
   'port': 22,
   'log_file_path' : '/var/log/pythian_portscan',
   'port_service_info_file_path' : 'config/port_services.csv'
}
