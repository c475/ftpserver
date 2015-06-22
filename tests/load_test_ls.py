import ftplib
import sys
import threading


def make_request(f):
    for i in xrange(1000):
        r.retrlines("LIST")
    f.close()


ftps = []

for i in xrange(1000):
    ftps.append(ftplib.FTP(("127.0.0.1", int(sys.argv[1])), "Daniel" + str(i), "Password"))

for f in ftps:
    t = threading.Thread(target=make_request, args=(f,))
    t.start()
