import socket  
import json
import ccrypto
from cbor2 import dumps, loads
from collections import OrderedDict 

class Platform:
    def __init__(self):
        self.authenticator_address = ('127.0.1.1', 23456)
        self.relying_party_address = ('127.0.1.1', 23457)

    def send_request(self, address, params, command):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        request = {}
        request['command'] = command
        request['params'] = params
        sock.sendall(str(request).encode())
        response = ''
        while True:
            response = response + sock.recv(2048).decode()
            break
        response = eval(response)
        print(response)
        return response  

    def register_u2f(self, website):
        user_pass = {
            "username": "steve", 
            "password": "not_secure"
        }
        response = self.send_request(self.relying_party_address, user_pass, "party_request_registration")
        appID = response['appID']
        if appID != website:         # Verify appID
            print("appID does not match requested website")
        else:
            print("appID verified")
        credential = self.send_request(self.authenticator_address, response, "authenticator_make_credential")
        self.send_request(self.relying_party_address, credential, "party_store_credential")
