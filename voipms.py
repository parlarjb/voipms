import httplib
import urllib
import json


class Voipms(object):
    api_url = "/api/v1/rest.php?%s"    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.conn = None

    def connect(self):
        self.conn = httplib.HTTPSConnection("voip.ms")

    def get_callerid_filtering(self, specific_id=''):
        '''
        specific_id is the voip.ms ID for a specific CallerID entry
        '''
        return self.method_call('getCallerIDFiltering', {'filtering':specific_id})

    def create_callerid_filter(self, callerid, routing_action, note=""):
        '''
        callerid: Phone number for the filter. Has to be a string
        routing_action: sys:hangup, sys:busy, etc.
        '''
        return self.method_call("setCallerIDFiltering", {'callerid':callerid, 'routing':routing_action, 'note':note})


    def method_call(self, method_name, params={}, action='GET', url=api_url):
        if self.conn:
            base_url = url % "api_username={username}&api_password={password}".format(username = self.username, password = self.password) + "&%s"
            params.update({'method':method_name})
            final_params = urllib.urlencode(params)
            self.conn.request(action, base_url % final_params) 
            return json.load(self.conn.getresponse())
        
