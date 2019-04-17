import random
import socket
from Server import Server

class RelyingParty(Server):
    def __init__(self):
        Server.__init__(self)
        self.server_port = 23457
        self.commands = {
            "request_registration": self.request_registration,
            "register_authenticator": self.register_authenticator,
        }
        self.webname = "example.com"
        self.users = {}

    def request_registration(self, params):
        response ={}
        challenge = random.randint(1,1000)
        appID = self.webname
        response['challenge'] = challenge
        response['appID'] = appID
        return response

    def register_authenticator(self, params):
        challenge = random.randint(1,1000)
        return challenge
    
r = RelyingParty()
r.listen()