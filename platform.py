import socket  
from cbor2 import dumps, loads
from collections import OrderedDict 

class Platform:
    def __init__(self):
        self.server_ip_address = '127.0.1.1'
        self.server_port = 23456        
        self.sock = None        

    def connect(self):
        # create TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.server_ip_address, self.server_port)  
        self.sock.connect(server_address)  
        print ("Connecting to %s:%s" % (self.server_ip_address, self.server_port))

    def send(self, msg):
        self.sock.sendall(msg)

    def receive(self):
        response = ''
        while True:
            response = response + self.sock.recv(1024).decode()
            break
        print(response)
        return response
        
    def disconnect(self):
        self.sock.close()  
    
    def get_authenticator_info(self):
        self.send(b'\x08\x02')
        self.receive()

    def ask_authenticator_make_credential(self):
        data = {
            1: b"\x68\x71\x34\x96\x82\x22\xec\x17\x20\x2e\x42\x50\x5f\x8e\xd2\xb1\x6a\xe2\x2f\x16\xbb\x05\xb8\x8c\x25\xdb\x9e\x60\x26\x45\xf1\x41",
            2: {
                "id": "example.com",
                "name": "Acme"
            },
            3: {
                "id": b"\x30\x82\x01\x93\x30\x82\x01\x38\xa0\x03\x02\x01\x02\x30\x82\x01\x93\x30\x82\x01\x38\xa0\x03\x02\x01\x02\x30\x82\x01\x93\x30\x82",
                "icon": "https://pics.example.com/00/p/aBjjjpqPb.png",
                "name":  "johnpsmith@example.com",
                "displayName": "John P. Smith"
            },
            4: [
                {
                    "alg": -7,
                    "type": "public-key"
                },
                {
                    "alg": -257,
                    "type": "public-key"
                }
            ],
            7: {
                "rk": True
            }
        }
        request = b'\x01' + dumps(data)
        print(request.hex())