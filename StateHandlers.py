class UserState(object):
    """
    This will finally come in handy.
    Keep state of user because of non-blocking sockets etc...
    """

    def __init__(self, request):
        self.request = request
        self.username = None
        self.authenticated = False


class ServerState(object):

    def __init__(self, request):
        self.request = request
        self.transfer_state = None
        self.type = "A"
        self.working_directory = "/"

    def change_directory(self, path):
        if path[0] == "/" or path[0] == "~":
            self.working_directory = path
        else:
            if path[-1] != "/":
                path += "/"
            
            self.working_directory = self.working_directory + path


class SystemInfo(object):

    def __init__(self, request):
        self.request = request


class SystemConfiguration(object):

    def __init__(self):
        self.buffersize = 1024


class DataChannel(object):

    def __init__(self, sys_config):
        self.sys_config = sys_config
        self.socket = None
        self.connected = False
        self.address = None

    def send(self, content):
        # BAD!!! maybe
        self.socket.send(content)

    def receive(self):
        # response = self.channel.recv(self.sys_config.buffersize)
        pass
