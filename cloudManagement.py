#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

from heatclient.client import Client

token='6c47095dd45d40f4bff5443c26044eb4'
tenant='mcntub'
tenant_id='64969ad482c643cb8439a55e648e5ebb'
heat_url='http://bart.cloudcomplab.ch:8004/v1/' + tenant_id

class CloudOrchestrator():
    def __init__(self, region):
        self.auth_token = self.get_auth_token()
        heat = Client('1', endpoint=heat_url, token=self.auth_token)
        self.stack_manager = heat.stacks        
        self.stack_id = self.get_stack_id()
        self.stack_list = []
        self.region = region
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
        self.auth_token = open('/home/ubuntu/authtoken', 'r').read().rstrip()
        return self.auth_token

    def get_stack_id(self):
        self.stack_id = open('/home/ubuntu/stackid', 'r').read().rstrip()
        return self.stack_id

    def create_stack(self):
        if self.stack_manager is None:
            self.__init__(self.auth_token)
        print "self.stack_manager.create()"

    def delete_stack(self):
        if self.stack_id is None :
            self.get_stack_id()
        self.stackManager.delete(self.stack_id)
