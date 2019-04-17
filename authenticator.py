import socket
import ccrypto
from Server import Server
from cbor2 import dumps, loads
from collections import OrderedDict 

class Authenticator(Server):
    def __init__(self):
        Server.__init__(self)
        self.server_port = 23456        
        self.commands = {
            'authenticator_make_credential': self.authenticator_make_credential,
        }
        
    def authenticator_make_credential(self, params):
        response ={}
        appID = params['appID']
        challenge = params['challenge']
        print("Request received to make new credential with the following data:")
        print("\tappID: ", appID)
        print("\tchallenge: ", challenge)
        # approve = input("Type 'y' to approve, anything else to deny: ")
        # if approve == 'y':
        #     print("Approved")
        #     result = ccrypto.generate_credential(appID, challenge)
        #     return str(result)
        # else:
        #     return "NotAllowedError"
        key, nonce = ccrypto.generate_credential(appID)
        mac = ccrypto.generate_mac(appID, key)
        publicKey = key.public_key().export_key(format='PEM')
        keyHandle = {
            'nonce': nonce,
            'mac': mac
        }
        toSign = OrderedDict([
            ('appID', appID),
            ('challenge', challenge),
            ('publicKey', publicKey),
            ('keyHandle', keyHandle)
        ])
        signature = ccrypto.sign(key, toSign)
        response['keyHandle'] = keyHandle
        response['publicKey'] = publicKey
        response['signature'] = signature
        return response

a = Authenticator()
a.listen()