import sys
import socket
import threading


# Reads command line inputs
# "-ip X.X.X.X" to set server's IP address
# "-v" to activate verbose mode
def inputs():
    HOST = None
    v = False
    for x in range(len(sys.argv)):
        if "-ip" in sys.argv[x]:
            HOST = sys.argv[x+1]
        if "-v" in sys.argv[x]:
            v = True
    return HOST, v


class Client(threading.Thread):

    def __init__(self, PORT, ID, target, fn, v=False, HOST="127.0.0.1"):

        self.PORT = PORT
        self.ID = ID
        self.target = target
        self.fn = fn
        self.v = v
        self.HOST = HOST
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sck.setblocking(3.0)
        threading.Thread.__init__(self)

    def run(self):

        # Connection
        sent = False
        while True:
            try:
                self.sck.connect((self.HOST, self.PORT))
            except ConnectionRefusedError:
                if not sent and self.v:
                    print(self.target, "is not online, trying again")
                    sent = True
            else:
                if self.v:
                    print(self.target, "is online, trying to connect")
                break

        # Identification
        if self.v:
            print(self.ID+" -> "+self.target+": |CON|"+self.ID+"|")
        try:
            self.sck.send(bytes("|CON|"+self.ID+"|", "utf-8"))
        except OSError:
            print(self.target+" disconnected")
            print(self.ID+" disconnecting from "+self.target)
            self.sck.close()
            sys.exit()

        # Reading identification acknowledge
        data = None
        while not data:
            try:
                data = self.sck.recv(1024)
            except Exception:
                pass
        if self.v:
            print(self.ID+" <- "+self.target+":", str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if data[1] == "ACK" and data[2] == "CON":
            # Running client specific function
            self.fn(self)
        else:
            self.sck.close()
            raise ValueError("acknowledge not recognized, aborting.")
