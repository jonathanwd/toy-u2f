import socket  
import json
import ccrypto
from cbor2 import dumps, loads
from collections import OrderedDict 

class Platform:
    def __init__(self):
        self.server_ip_address = '127.0.1.1'
        self.server_port = 23456        
        self.sock = None        

    def connect(self, ip, port):
        # create TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)  
        self.sock.connect(server_address)  
        print ("Connecting to %s:%s" % (ip, port))

    def send(self, msg):
        self.sock.sendall(msg)

    def receive(self):
        response = ''
        while True:
            response = response + self.sock.recv(2048).decode()
            break
        print(response)
        return response
        
    def disconnect(self):
        self.sock.close()  

    def get_authenticator_info(self):
        self.send(b'\x08\x02')
        self.receive()

    def ask_authenticator_make_credential(self):
        self.appID = OrderedDict([
                ("id", "example.com"),
                ("name", "Acme")])
        
        data = {
            1: b"\x68\x71\x34\x96\x82\x22\xec\x17\x20\x2e\x42\x50\x5f\x8e\xd2\xb1\x6a\xe2\x2f\x16\xbb\x05\xb8\x8c\x25\xdb\x9e\x60\x26\x45\xf1\x41",
            2: self.appID,
            3: OrderedDict([
                ("id", b"\x30\x82\x01\x93\x30\x82\x01\x38\xa0\x03\x02\x01\x02\x30\x82\x01\x93\x30\x82\x01\x38\xa0\x03\x02\x01\x02\x30\x82\x01\x93\x30\x82"),
                ("icon", "https://pics.example.com/00/p/aBjjjpqPb.png"),
                ("name",  "johnpsmith@example.com"),
                ("displayName", "John P. Smith")
            ]),
            4: [
                OrderedDict([
                    ("alg", -7),
                    ("type", "public-key")
                ]),
                OrderedDict([
                    ("alg", -257),
                    ("type", "public-key")
                ])
            ],
            7: {
                "rk": True
            }
        }
        request = b'\x01' + dumps(data)
        # print(request.hex())
        self.send(request)
    
    def receive_attestation(self):
        response = self.receive()
        attestation = json.loads(response)
        public_key = attestation['publicKey']
        signature = attestation['app_id_sig']
        app_id = str(self.appID)
        print("Response received")
        print("Validating signature...")
        ccrypto.verify(public_key, signature, app_id)
        # print(attestation)