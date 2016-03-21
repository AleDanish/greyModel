#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

from heatclient.client import Client
import keystoneclient.v2_0.client as ksclient
from heatclient.common import template_utils

tenant_name='mcntub'
tenant_id='64969ad482c643cb8439a55e648e5ebb'
heat_url='http://bart.cloudcomplab.ch:8004/v1/' + tenant_id
keystone_credentials = {
    'username': 'alessandropernafini',
    'password': 'unib0bart',
    'tenant_name': 'mcntub',
    'auth_url': 'http://bart.cloudcomplab.ch:5000/v2.0'
}
stack_name="teststack influxdb-cyclops2"
template_file="influxdb.yaml"

class HeatClient():
    def __init__(self, region_name):
        self.region_name = region_name
        self.auth_token = self.get_auth_token()
        if region_name == None:
            print "senza region"
            heat_credentials = {
                'endpoint': heat_url,
                'token': self.auth_token
            }
        else:
            print "con region: ", region_name
            heat_credentials = {
                'endpoint': heat_url,
                'token': self.auth_token,
                'region_name': self.region_name
            }
        heat = Client('1', **heat_credentials)
        self.stack_manager = heat.stacks        
        self.stack_id = self.get_stack_id()
        self.stack_list = []
        self.auth_token = self.get_auth_token()

    def get_stack_list(self):
        if self.stack_manager is None:
            self.__init__(self.auth_token)
        stack_generator = self.stack_manager.list()
        self.stack_list = [x for x in stack_generator]
        return self.stack_list

    def get_stack(self):
        if self.stack_id is None:
            self.get_stack_id()
        if not self.stack_list:
            self.stack_list = self.get_stack_list()
        for stack in self.stack_list:
            if stack.id == self.stack_id:
                return stack
        return None

    def get_auth_token(self):
        keystone = keystoneclient.v2_0.client.Client(**keystone_credentials)
        token = keystone.auth_ref['token']['id']
        self.auth_token = token
        return token

    def get_stack_id(self):
        self.stack_id = open('/home/ubuntu/stackid', 'r').read().rstrip()
        return self.stack_id

    def create_stack(self):
        if self.stack_manager is None:
            self.__init__(self.auth_token)
        tpl_files, template = template_utils.get_template_contents(template_file)
        params = {
            'stack_name': stack_name,
            'template': template
        }
        self.stack_manager.validate(**params)
        self.stack_manager.create(**params)

    def delete_stack(self):
        if self.stack_id is None :
            self.stack_id = self.get_stack_id()
        self.stack_manager.delete(self.stack_id)
