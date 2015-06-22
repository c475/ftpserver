import ftplib
import sys
import threading

ftps = []
port = int(sys.argv[1])


def make_request(f):
    f.set_debuglevel(2)
    f.connect("127.0.0.1", port)
    welcome = f.getwelcome()
    f.login("Daniel", "Cool")
    f.set_pasv(False)

    for i in xrange(1000):
        f.transfercmd("LIST")

    f.close()


for i in xrange(1):
    ftps.append(ftplib.FTP())

for f in ftps:
    t = threading.Thread(target=make_request, args=(f,))
    t.start()
