import socket

class Server:
    def __init__(self):
        self.server_ip_address = '127.0.1.1'
        self.server_port = 23456        
        self.sock = None 
        self.commands = {}
    
    def receive(self, connection):
        response = ''
        while True:
            response = response + connection.recv(4096).decode()
            break
        print(response)
        return response

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
                    request = eval(self.receive(connection))
                    print(request)
                    function = request['command']
                    params = request['params']
                    if function in self.commands:
                        f = self.commands[function]
                    else:
                        f = self.unknown_request
                    print ("Request: %s" % f.__name__)
                    response = f(params)
                    connection.send(str(response).encode())
                    print("Response: %s" % response)
                    break
            finally:
                connection.close()

    def unknown_request(self, params):
        return "unknown request"
