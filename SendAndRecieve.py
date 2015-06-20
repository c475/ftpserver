class SendAndReceive(object):

    def __init__(self, clientsocket, config):
        self.clientsocket = clientsocket
        self.config = config
        self.last_response = None

    def receive(self, split=True):
        """
        Does a .recv().
        Split the command and params into a list by default.
        Otherwise, return a command string.
        """
        if split is True:
            self.last_response = self.clientsocket.recv(self.config.buffersize)

            if not self.last_response:
                return self.last_response

            self.last_response = self.last_response.strip().split(" ")
            print(self.last_response)
            return self.last_response
        else:
            self.last_response = self.clientsocket.recv(self.config.buffersize)

            if not self.last_response:
                return self.last_response

            self.last_response = self.last_response.strip()
            print(self.last_response)
            return self.last_response

    def send(self, payload):
        try:
            self.clientsocket.sendall(payload)
            return True
        except:
            # socket is no longer listening
            print("Connection closed or something? Let's see")
            return False
