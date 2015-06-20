import socket
import select


class SocketServer(object):
    """
    Spawns client sockets to handle new requests to ftp server.
    Also, implement access controls.
    """

    def __init__(self, address, request_handler):
        self.host, self.port = address

        self.serversocket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.serversocket.setblocking(0)

        self.serversocket.bind((self.host, self.port))

        # request handlef class, and a dict of handlers for each socket connection
        self.request_handler = request_handler
        self.handlers = {}

        # make the number of listens configurable eventually
        self.serversocket.listen(5)

        self.readable = [self.serversocket]
        self.writable = []
        self.erroring = []

    def serve_forever(self):
        while self.readable:

            read, write, error = select.select(
                self.readable,
                self.writable,
                self.erroring
            )

            self.handle_reads(read)
            self.handle_write(write)
            self.handle_error(error)


    def handle_reads(self, read):
        for s in read:

            # someone is making a connection
            if s is self.serversocket:
                clientsocket, address = s.accept()
                clientsocket.setblocking(0)

                # add to list of writable sockets
                self.readable.append(clientsocket)

                # instantiate a request handler class for the socket
                self.handlers[clientsocket] = self.request_handler(
                    clientsocket,
                    Queue.Queue()
                )

            # it's an open client socket...
            else:
                # handle request
                success = self.handlers[s].handle_read()

                if success:
                    # add it to writable sockets for response if it isn't in there
                    if s not in self.writable:
                        self.writable.append(s)

                # we're talking to a closed socket, or something went very wrong
                else:
                    # remove from writable sockets
                    if s in self.writable:
                        self.writable.remove(s)

                    self.readable.remove(s)

                    s.close()

                    # remove he message queue
                    del self.handlers[s]

    def handle_writes(self, write):
        for s in write:
            try:
                # message = self.handlers.queue.get_nowait()
                self.handlers[s].handle_write()
            # no messages are waiting so stop checking
            except Queue.Empty:
                # no messages waiting
                # i dont think its the right thing to do to remove it but whatever
                self.readable.remove(s)
            else:
                s.send(message)

    def handle_error(self, error):
        for s in error:
            # stop listening to this socket
            pass
