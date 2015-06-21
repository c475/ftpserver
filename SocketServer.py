import socket
import select
import Queue

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

            print("read: " + str(read))
            print("write: " + str(write))
            print("error: " + str(error))

            self.handle_reads(read)
            self.handle_write(write)
            self.handle_error(error)


    def handle_reads(self, read):
        for s in read:

            # someone is making a connection
            if s is self.serversocket:
                clientsocket, address = s.accept()
                print("accepted new connection from: " + str(address))
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
                print("handling read for socket: " + str(s))
                # handle request
                success = self.handlers[s].handle_read()

                if success:
                    # add it to writable sockets for response if it isn't in there
                    if s not in self.writable:
                        print("adding it to writable.")
                        self.writable.append(s)

                # we're talking to a closed socket, or something went very wrong
                else:
                    print("closing socket: " + str(s))
                    # remove from writable sockets
                    if s in self.writable:
                        self.writable.remove(s)

                    self.readable.remove(s)

                    s.close()

                    # remove he message queue
                    del self.handlers[s]

    def handle_write(self, write):
        for s in write:
            try:
                print("handling write event for socket: " + str(s))
                # message = self.handlers.queue.get_nowait()
                self.handlers[s].handle_write()
            # no messages are waiting so stop checking
            except Queue.Empty:
                # remove from writable until we get a read from it...
                self.writable.remove(s)

    def handle_error(self, error):
        for s in error:
            print("socket is in error: " + str(s))
            # stop listening to this socket
            pass
