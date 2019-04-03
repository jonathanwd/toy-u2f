import socket

class Authenticator:
    def __init__(self):
        self.server_ip_address = '127.0.1.1'
        self.server_port = 23456        
        self.sock = None 
        self.commands = {
            'authenticatorGetInfo': self.authenticator_get_info
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
                    request = connection.recv(1024).decode()
                    if request in self.commands:
                        f = self.commands[request]
                    else:
                        f = self.unknown_request
                    print ("Request: %s" % request)
                    response = f()
                    connection.send(response.encode())
                    print("Response: %s" % response)
                    break
            finally:
                connection.close()

    def authenticator_get_info(self):
        return "request received"
    
    def unknown_request(self):
        return "unknown request"

a = Authenticator()
a.listen()