import datetime

class SendAndReceive(object):

    def __init__(self, clientsocket, config):
        self.clientsocket = clientsocket
        self.config = config

        self.session_history = {}
        self.previous_message = None

        self.counter = 0

    def receive(self, split=True):
        """
        Does a .recv().
        Split the command and params into a list by default.
        Otherwise, return a command string.
        """
        if split is True:
            self.previous_message = self.clientsocket.recv(self.config.buffersize)

            if not self.previous_message:
                return self.previous_message

            self.previous_message = self.previous_message.strip().split(" ")
            print(self.previous_message)
        else:
            self.previous_message = self.clientsocket.recv(self.config.buffersize)

            if not self.previous_message:
                return self.previous_message

            self.previous_message = self.previous_message.strip()
            print(self.previous_message)

        self.session_history[self.counter] = self.previous_message

        self.counter += 1

        return self.previous_message

    def send(self, payload):
        try:
            self.clientsocket.sendall(payload)
            return True
        except:
            # socket is no longer listening
            print("Connection closed or something? Let's see")
            return False
