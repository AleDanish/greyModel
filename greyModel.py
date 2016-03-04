from py4j.java_gateway import JavaGateway
from py4j.java_collections import SetConverter, MapConverter, ListConverter
import time
import random
from zabbix_api import APIConnector

zabbix_url='http://137.204.57.236:8008/zabbix/'
zabbix_user='azanni'
zabbix_pass='azanni'

class MyList(list):
    def append(self, item):
        list.append(self, item)        
        if len(self) > 5: self[:1]=[]

def getGreyModelValues(composedList):
    values = []
    for list_py in composedList:
        list_java = ListConverter().convert(list_py, gateway._gateway_client)
        nextValue = gateway.entry_point.nextValue(list_java)
        values.append(float("{0:.4f}".format(nextValue)))
    return values

gateway = JavaGateway()
connector = APIConnector()
auth = connector.auth_zabbix()
host_ids = connector.get_zbx_hostids()
hosts_cpu_load = []
hosts_cpu_util = []
hosts_mem = []
for host in host_ids:
    hosts_cpu_load.append(MyList())
    hosts_cpu_util.append(MyList())
    hosts_mem.append(MyList())

while True:
    cpu_loads = connector.get_cpu_load()
    cpu_util = connector.get_cpu_util()
    mem = connector.get_mem_load()
    for i in range(len(host_ids)):
        hosts_cpu_load[i].append(cpu_loads[i])
        hosts_cpu_util[i].append(cpu_util[i])
        hosts_mem[i].append(mem[i])
    print "zbx - cpu_load: ", hosts_cpu_load
    print "zbx - cpu_util: ", hosts_cpu_util
    print "zbx - mem: ", hosts_mem

    cpu_load_GM = getGreyModelValues(hosts_cpu_load)
    cpu_util_GM = getGreyModelValues(hosts_cpu_util)
    mem_GM = getGreyModelValues(hosts_mem)
    print "next value GM - cpu_load: ", cpu_load_GM
    print "next value GM - cpu_util: ", cpu_util_GM
    print "next value GM - mem: ", mem_GM
    time.sleep(50)
