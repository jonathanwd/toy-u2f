import socket
import ccrypto
from cbor2 import dumps, loads

class Authenticator:
    def __init__(self):
        self.server_ip_address = '127.0.1.1'
        self.server_port = 23456        
        self.sock = None 
        self.commands = {
            b'\x01': self.authenticator_make_credential,
            # b'\x01': self.unknown_request,
            b'\x02': self.authenticator_get_assertion,
            b'\x04': self.authenticator_get_info,
            b'\x06': self.authenticator_client_PIN,
            b'\x07': self.authenticator_reset,
            b'\x08': self.authenticator_get_next_assertion
        }

    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.server_ip_address, self.server_port)  
        self.sock.bind(server_address)
        print ("Listening on %s:%s" % (self.server_ip_address,self.server_port))
        self.sock.listen(1)
        while True:  
            print ('Waiting for a connection')
            connection, client_address = self.sock.accept()
            try:
                print ('Connection from', client_address)
                while True:
                    request = connection.recv(1024)
                    function = request[:1]
                    params = request[1:]
                    if function in self.commands:
                        f = self.commands[function]
                    else:
                        f = self.unknown_request
                    print ("Request: %s" % f.__name__)
                    response = f(params)
                    connection.send(response.encode())
                    print("Response: %s" % response)
                    break
            finally:
                connection.close()

    def authenticator_make_credential(self, params):
        p = {}
        dom = loads(params)
        p["hash"] = dom[1]
        p["rpEntity"] = dom[2]
        p["userEntity"] = dom[3]
        p["credTypesAndPubKeyAlgs"] = dom[4]
        p["options"] = dom[7]
        
        print("Request received to make new credential with the following data:")
        print("\trp id: " + p["rpEntity"]["id"])
        print("\trp name: " + p["rpEntity"]["name"])
        print("\tuser name: " + p["userEntity"]["name"])
        print("\tuser displayName: " + p["userEntity"]["displayName"])
        approve = input("Type 'y' to approve, anything else to deny: ")
        if approve == 'y':
            print("Approved")
            algorithm = p["credTypesAndPubKeyAlgs"][0]["alg"]
            result = ccrypto.generate_credential(algorithm, p['rpEntity'], p['userEntity'])
            return str(result)
        else:
            return "NotAllowedError"

    def authenticator_get_assertion(self, params):
        # rpId, clientDataHash
        return 'okok'

    def authenticator_get_next_assertion(self, params):
        return 'okokok'

    def authenticator_get_info(self, params):
        # versions, aaguid
        return "okokokok"

    def authenticator_client_PIN(self, params):
        # pinProtocol, subCommand
        return "okokokokok"
    
    def authenticator_reset(self, params):
        return "okokokokokok"

    def unknown_request(self, params):
        return "unknown request"

a = Authenticator()
a.listen()