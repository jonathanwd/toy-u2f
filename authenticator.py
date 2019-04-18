import socket
import ccrypto
from Server import Server
from cbor2 import dumps, loads
from collections import OrderedDict 

class Authenticator(Server):
    def __init__(self):
        Server.__init__(self)
        self.server_port = 23456
        self.counter = 0        
        self.commands = {
            'authenticator_make_credential': self.authenticator_make_credential,
            'authenticator_authenticate': self.authenticator_authenticate,
        }
        
    def test_user_presence(self):
        approve = input("Type 'y' to approve, anything else to deny: ")
        if approve == 'y':
            print("Approved")
            return True
        else:
            print('Denied')
            return False

    def authenticator_make_credential(self, params):
        response = {}
        appID = params['appID']
        challenge = params['challenge']
        print("Request received to make new credential with the following data:")
        print("\tappID: ", appID)
        print("\tchallenge: ", challenge)
        if not self.test_user_presence():
            return {'Error': 'User presense failed'}
        key, nonce = ccrypto.new_credential(appID)
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
    
    def authenticator_authenticate(self, params):
        response ={}
        appID = params['appID']
        challenge = params['challenge']
        keyHandle = params['keyHandle']
        print("Request received to make authenticate with the following data:")
        print("\tappID: ", appID)
        print("\tchallenge: ", challenge)
        if not self.test_user_presence():
            return {'Error': 'User presense failed'}
        key = ccrypto.credential_from_nonce(appID, keyHandle['nonce'])
        mac = ccrypto.generate_mac(appID, key)
        if mac != keyHandle['mac']:
            print("keyHandle hash does not match.")
        else:
            self.counter = self.counter + 1
            toSign = OrderedDict([
                ('appID', appID),
                ('challenge', challenge),
                ('counter', self.counter)
            ])
            signature = ccrypto.sign(key, toSign)
            response['counter'] = self.counter
            response['signature'] = signature
        return response

a = Authenticator()
a.listen()