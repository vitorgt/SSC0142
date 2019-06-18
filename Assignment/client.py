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

    def __init__(self, PORT, ID, fn, v=False, HOST="127.0.0.1"):

        self.PORT = PORT
        self.ID = ID
        self.fn = fn
        self.v = v
        self.HOST = HOST
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):

        # Connection
        while True:
            try:
                self.sck.connect((self.HOST, self.PORT))
            except ConnectionRefusedError:
                print("Server is not online, trying again")
            else:
                break

        # Identification
        if self.v:
            print(self.ID, "sending:  |CON|"+self.ID+"|")
        self.sck.send(bytes("|CON|"+self.ID+"|", "utf-8"))

        # Reading identification acknowledge
        while True:
            data = self.sck.recv(1024)
            if data:
                break
        data = str(data, "utf-8").split("|")
        if self.v:
            print(self.ID, "received:", data)
        if data[1] == "ACK" and data[2] == "CON" and data[3] == self.ID:
            # Running client specific function
            self.fn(self)
        else:
            self.sck.close()
            raise ValueError("acknowledge not recognized, aborting.")
