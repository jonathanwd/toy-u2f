import random
import socket
import ccrypto
from Server import Server
from collections import OrderedDict 

class RelyingParty(Server):
    def __init__(self):
        Server.__init__(self)
        self.server_port = 23457
        self.commands = {
            "party_request_registration": self.request_registration,
            "party_store_credential": self.store_credential,
        }
        self.webname = "example.com"
        self.users = {
            "steve": {
                "password": "not_secure",
            }
        }

    def request_registration(self, params):
        username = params['username']
        password = params['password']
        response = {}
        if username in self.users:
            if password == self.users[username]['password']:
                self.current_challenge = random.randint(1,1000)
                appID = self.webname
                response['challenge'] = self.current_challenge
                response['appID'] = appID
                self.current_user = username
        return response

    def store_credential(self, params):
        response = {'response': 'Signature unverified'}
        signature = params['signature']
        keyHandle = params['keyHandle']
        publicKey = params['publicKey']
        toSign = OrderedDict([
            ('appID', self.webname),
            ('challenge', self.current_challenge),
            ('publicKey', publicKey),
            ('keyHandle', keyHandle)
        ])
        if ccrypto.verify(publicKey, signature, toSign):
            user_info = {
                'publicKey': publicKey,
                'keyHandle': keyHandle
            }
            self.users[self.current_user]['u2f'] = user_info
            response = {'response': 'U2F device registered'}
        self.current_challenge = -1
        self.current_user = -1
        return response
    
r = RelyingParty()
r.listen()