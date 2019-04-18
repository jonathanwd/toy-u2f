import random
import socket
import ccrypto
from Server import Server
from collections import OrderedDict 

class RelyingParty(Server):
    def __init__(self, webname, port):
        Server.__init__(self)
        self.server_port = port
        self.commands = {
            "party_request_registration": self.request_registration,
            "party_store_credential": self.store_credential,
            "party_request_authentication": self.request_authentication,
            "party_check_authentication": self.check_authentication,
            "party_sign_up": self.sign_up,
        }
        self.webname = webname
        self.users = {
            "steve": {
                "password": "not_secure"
            }
        }

    def sign_up(self, params):
        username = params['username']
        password = params['password']
        if username in self.users:
            return {'Error': 'User already exists'}
        else:
            info = {"password": password}
            self.users[username] = info
            msg = username + ' signed up successfully'
            return {'response': msg}

    def request_registration(self, params):
        username = params['username']
        password = params['password']
        response = {'Error': 'Bad username/password'}
        if username in self.users:
            if password == self.users[username]['password']:
                self.current_challenge = random.randint(1,1000)
                appID = self.webname
                response = {
                    'challenge': self.current_challenge,
                    'appID': appID
                }
                self.current_user = username
        return response

    def store_credential(self, params):
        response = {'Error': 'Signature unverified'}
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
                'keyHandle': keyHandle,
                'counter': -1
            }
            self.users[self.current_user]['u2f'] = user_info
            response = {'response': 'U2F device registered'}
        self.current_challenge = -1
        self.current_user = -1
        return response
    
    def request_authentication(self, params):
        username = params['username']
        password = params['password']
        response = {'Error': 'Username/password unregistered'}
        if username in self.users:
            if password == self.users[username]['password'] and 'u2f' in self.users[username]:
                self.current_challenge = random.randint(1,1000)
                appID = self.webname
                keyHandle = self.users[username]['u2f']['keyHandle']
                response = {
                    'challenge': self.current_challenge,
                    'appID': appID,
                    'keyHandle': keyHandle
                }
                self.current_user = username
        return response
    
    def check_authentication(self, params):
        response = {'Error': 'Signature unverified'}
        signature = params['signature']
        counter = params['counter']
        publicKey = self.users[self.current_user]['u2f']['publicKey']
        toSign = OrderedDict([
            ('appID', self.webname),
            ('challenge', self.current_challenge),
            ('counter', counter),
        ])
        if ccrypto.verify(publicKey, signature, toSign):
            response = {'response': 'Successful authentication'}
        self.current_challenge = -1
        self.current_user = -1
        return response       

r = RelyingParty("example.com", 23457)
r.listen()