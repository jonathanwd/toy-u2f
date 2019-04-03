import socket

class Authenticator:
    def __init__(self):
        self.server_ip_address = '127.0.1.1'
        self.server_port = 23456        
        self.sock = None 
        self.commands = {
            # b'\x01': self.authenticator_make_credential,
            b'\x01': self.unknown_request,
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
                    prams = request[1:]
                    if function in self.commands:
                        f = self.commands[function]
                    else:
                        f = self.unknown_request
                    print ("Request: %s" % f.__name__)
                    response = f()
                    connection.send(response.encode())
                    print("Response: %s" % response)
                    break
            finally:
                connection.close()
    
    def authenticator_make_credential(self, clientDataHash, rp, user, pubKeyCredParams):
        return "ok"

    def authenticator_get_assertion(self, rpId, clientDataHash):
        return 'okok'

    def authenticator_get_next_assertion(self):
        return 'okokok'

    def authenticator_get_info(self, versions, aaguid):
        return "okokokok"

    def authenticator_client_PIN(self, pinProtocol, subCommand):
        return "okokokokok"
    
    def authenticator_reset(self):
        return "okokokokokok"

    def unknown_request(self):
        return "unknown request"

a = Authenticator()
a.listen()