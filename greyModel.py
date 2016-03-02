from py4j.java_gateway import JavaGateway
from py4j.java_collections import SetConverter, MapConverter, ListConverter
import time
import random

class MyList(list):
    def append(self, item):
        list.append(self, item)        
        if len(self) > 5: self[:1]=[]

gateway = JavaGateway()
values_py = MyList()
while True:
    
    val = random.uniform(0.0, 10.0) # input from MaaS
    print val
    values_py.append(val)
    print values_py
    values_java = ListConverter().convert(values_py, gateway._gateway_client)
    nextValue = gateway.entry_point.nextValue(values_java)
    print "nextValue: %s" %nextValue
    time.sleep(1)
