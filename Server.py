import socket
import select
import Queue
import types


class Server(object):

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

                # initialize the FTP session (SERVICE_READY_NEW_USER)
                self.handlers[clientsocket].initialize_ftp()

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

    def handle_write(self, write):
        for s in write:
            try:
                resp = self.handlers[s].handle_write()

                # think about passing socket objects back to server
                if isinstance(resp, socket.socket):
                    pass

            # no messages are waiting so stop checking
            # kinda ignoring a problem here with very high loads/broken sockets
            except:
                # remove from writable until we get a read from it...
                self.writable.remove(s)

    def handle_error(self, error):
        for s in error:
            print("socket is in error: " + str(s))
            # stop listening to this socket
            pass

    def shutdown(self):
        for s in self.erroring:
            self.erroring.remove(s)
            s.close()

        for s in self.writable:
            self.writable.remove(s)
            s.close()

        for s in self.readable:
            if s is not self.serversocket:
                self.readable.remove(s)
                s.close()

        self.readable.remove(self.serversocket)
        self.serversocket.close()
