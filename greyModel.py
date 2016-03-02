from py4j.java_gateway import JavaGateway
from py4j.java_collections import SetConverter, MapConverter, ListConverter
import time
import random
from zabbix.api import ZabbixAPI

class MyList(list):
    def append(self, item):
        list.append(self, item)        
        if len(self) > 5: self[:1]=[]

zabbix_url='http://137.204.57.236:8008/zabbix/'
zabbix_user='azanni'
zabbix_pass='azanni'

gateway = JavaGateway()
values_py = MyList()
while True:
    
    zapi = ZabbixAPI(url=zabbix_url, user=zabbix_user, password=zabbix_pass)

    val = random.uniform(0.0, 10.0) # input from MaaS
    print val
    values_py.append(val)
    print values_py
    values_java = ListConverter().convert(values_py, gateway._gateway_client)
    nextValue = gateway.entry_point.nextValue(values_java)
    print "nextValue: %s" %nextValue
    time.sleep(1)
