import sys
import optparse

from Server import Server
from RequestHandlers import FTPRequestHandler


if __name__ == "__main__":

    try:
        port = int(sys.argv[1])
    except:
        sys.exit()

    server = Server(("127.0.0.1", port), FTPRequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit()
