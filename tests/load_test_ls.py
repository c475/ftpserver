import socket
import random
import threading
import sys
import time


allports = []

def make_request(sock, host, port):
    sock.connect((host, port))

    # initialization message
    d = sock.recv(1024)

    sock.send("USER daniel")

    # user OK
    d = sock.recv(1024)

    sock.send("PASS coolguy")

    # password OK
    d = sock.recv(1024)

    sock.send("SYST")

    # UNIX
    d = sock.recv(1024)

    for i in xrange(10000):
        p1 = random.randint(144, 237)
        p2 = random.randint(144, 237)
        pp = (p1 * 256) + p2

        while pp in allports:
            p1 = random.randint(144, 237)
            p2 = random.randint(144, 237)
            pp = (p1 * 256) + p2

        allports.append(pp)

        data_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_channel.bind(("127.0.0.1", pp))

        sock.send("PORT 127,0,0,1," + str(p1) + "," + str(p2))

        # COMMAND_OK
        d = sock.recv(1024)

        sock.send("LIST")

        # FILE_STATUS_OK
        d = sock.recv(1024)


        data_channel.listen(5)
        newsock, addr = data_channel.accept()
        print("accepted connection from: " + str(addr))

        # receive LIST results
        li = newsock.recv(2048)

        # CLOSING CONNECTION
        d = sock.recv(1024)

        newsock.close()

    sock.close()

threads = []

for i in xrange(10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    threads.append(
        threading.Thread(
            target=make_request,
            args=(s, "127.0.0.1", int(sys.argv[1]))
        )
    )

for thread in threads:
    thread.start()
