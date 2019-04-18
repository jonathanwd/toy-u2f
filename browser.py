import socket  
import json
import ccrypto
from cbor2 import dumps, loads
from collections import OrderedDict 

class Browser:
    def __init__(self):
        self.authenticator_address = ('127.0.1.1', 23456)

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
        return response  

    def register_u2f(self, website, username, password, address):
        user_pass = {
            "username": username, 
            "password": password
        }
        response = self.send_request(address, user_pass, "party_request_registration")
        if "Error" in response:
            return response
        appID = response['appID']
        if appID != website:         # Verify appID
            return{"Error": "appID does not match requested website"}
        else:
            print("appID verified")
        credential = self.send_request(self.authenticator_address, response, "authenticator_make_credential")
        if "Error" in credential:
            return credential
        return self.send_request(address, credential, "party_store_credential")

    def authenticate_u2f(self, website, username, password, address):
        user_pass = {
            "username": username, 
            "password": password
        }
        response = self.send_request(address, user_pass, "party_request_authentication")
        if "Error" in response:
            return response
        appID = response['appID']
        if appID != website:         # Verify appID
            return{"Error": "appID does not match requested website"}
        else:
            print("appID verified")
        auth_sig = self.send_request(self.authenticator_address, response, "authenticator_authenticate")
        if "Error" in auth_sig:
            return auth_sig
        return self.send_request(address, auth_sig, "party_check_authentication")

    def sign_up(self, website, username, password, address):
        user_pass = {
            "username": username, 
            "password": password
        }
        return self.send_request(address, user_pass, "party_sign_up")
