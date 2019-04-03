import socket

class Authenticator:
    def __init__(self):
        self.server_ip_address = '127.0.1.1'
        self.server_port = 23456        
        self.sock = None 

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
                    data = connection.recv(1024)
                    if data:
                        print ("Data: %s" % data)
                    else:
                        print ("no more data.")
                        break
            finally:
                connection.close()

a = Authenticator()
a.listen()