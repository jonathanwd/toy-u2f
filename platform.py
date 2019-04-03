import socket  

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
        self.sock.sendall(msg.encode())

    def disconnect(self):
        self.sock.close()  