import socket  
import json
import ccrypto
from cbor2 import dumps, loads
from collections import OrderedDict 

class Platform:
    def __init__(self):
        self.server_ip_address = '127.0.1.1'
        self.authenticator_port = 23456       
        self.relying_party_port = 23457       
        self.sock_authenticator = None        
        self.sock_relying_party = None        
        self.sock = None        

    def connect(self):
        # create TCP/IP socket
        self.sock_authenticator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_relying_party = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.server_ip_address, self.authenticator_port)  
        self.sock_authenticator.connect(server_address)  
        print ("Connected to %s:%s" % (self.server_ip_address, self.authenticator_port))
        server_address = (self.server_ip_address, self.relying_party_port)  
        self.sock_relying_party.connect(server_address)  
        print ("Connected to %s:%s" % (self.server_ip_address, self.relying_party_port))

    def send(self, msg):
        self.sock.sendall(str(msg).encode())

    def receive(self):
        response = ''
        while True:
            response = response + self.sock.recv(2048).decode()
            break
        # print(response)
        return response
        
    def disconnect(self):
        self.sock_authenticator.close()  
        self.sock_relying_party.close()  

    def request_registration(self, website):
        request = {}
        request['command'] = "request_registration"
        request['params'] = []
        self.sock = self.sock_relying_party
        msg = request
        self.send(msg)
        response = eval(self.receive()) # returns the challenge and appID
        return response

    def register_u2f(self, website):
        response = self.request_registration(website)
        appID = response['appID']
        if appID != website:         # Verify appID
            print("appID does not match requested website")
        else:
            print("appID verified")
        self.request_authenticator_make_credential(response)

    def request_authenticator_make_credential(self, params):
        request = {}
        self.sock = self.sock_authenticator
        request['command'] = "authenticator_make_credential"
        request['params'] = params
        self.send(request)
        response = eval(self.receive())
        print(response)


    def receive_attestation(self):
        response = self.receive()
        attestation = json.loads(response)
        publicKey = attestation['publicKey']
        signature = attestation['app_id_sig']
        print("Response received")
        print("Validating signature...")
        ccrypto.verify(publicKey, signature, app_id)
        # print(attestation)