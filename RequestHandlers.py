import StateHandlers
from FTPCommander import FTPCommander

from responses import (
    SERVICE_READY_NEW_USER,
    SYNTAX_ERROR_COMMAND,
    SYNTAX_ERROR_PARAMS
)

from SendAndReceive import SendAndReceive


class FTPRequestHandler(object):

    def __init__(self, clientsocket, queue):
        self.clientsocket = clientsocket

        self.queue = queue

        # information about the current state of the user (username, etc)
        self.user = StateHandlers.UserState(self.clientsocket)

        # information about the current state of the system
        # user interation will change the state
        self.server_state = StateHandlers.ServerState(self.clientsocket)

        # information about the system, will probably axe this
        self.sys_info = StateHandlers.SystemInfo(self.clientsocket)

        # system configuration, pulled from the JSON config file
        self.sys_config = StateHandlers.SystemConfiguration()

        # data structure that models the "data channel" for transfers
        self.data_channel = StateHandlers.DataChannel(self.sys_config)

        # born to handle FTP commands
        self.commander = FTPCommander(
            self.clientsocket,
            self.user,
            self.sys_info,
            self.server_state,
            self.data_channel
        )

        self.transport = SendAndReceive(
            self.clientsocket,
            self.sys_config
        )

        self.queue.put(SERVICE_READY_NEW_USER)

    def handle_read(self):
        """
        Returns True if request is successfully handled.
        False if there was an error in handling the request.
        If response, add it
        """

        response = self.commander.receive()

        if not response:
            return False

        # just put the response in the queue until the socket is ready for writing
        self.queue.put(response)

        return True

    def handle_write(self):
        message = self.queue.get_nowait()

        try:
            command = message[0].upper()
        except IndexError:
            self.transport.send(SYNTAX_ERROR_COMMAND)

        if hasattr(self.commander, command):
            self.transport.send(getattr(self.commander, command)(message[1:]))
        else:
            self.transport.send(SYNTAX_ERROR_COMMAND)

    def finish(self):
        pass
