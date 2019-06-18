import sys
import atexit
import socket
import threading


# Thread wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        # lighter thread flag, kills thread when main thread dies
        thread.daemon = True
        thread.start()
    return wrapper


# Each new connection opens a new server thread
class ServerThread(threading.Thread):

    def __init__(self, manager, conn, addr):
        self.manager = manager
        self.conn = conn
        self.addr = addr[0]
        print("New connection with", self.addr)
        # When exiting application, close connection
        atexit.register(ServerThread.closeConn, self)
        threading.Thread.__init__(self)

    def closeConn(self):
        print("Closing connection with", self.addr)
        self.conn.close()
        sys.exit(0)

    def run(self):
        self.manager.fn(self)


class Server:

    @threaded
    def connectionsListener(self):
        while True:
            conn, addr = self.server.accept()
            ServerThread(manager=self, conn=conn, addr=addr).start()

    # Tries to close server
    def closeServer(self):
        try:
            self.server.close()
        except Exception as e:
            print("Server could not be closed because of", e)
            print("Closing application anyway")
        else:
            print("Server successfully closed")

    def __init__(self, PORT, fn):

        self.PORT = PORT
        self.fn = fn

        # Reading command line inputs
        # "-v" to activate verbose mode
        self.v = False
        for x in range(len(sys.argv)):
            if "-v" in sys.argv[x]:
                self.v = True

        # Opens socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', self.PORT))  # '' to accept any connection
        self.server.listen()

        # When exiting application, close server
        atexit.register(Server.closeServer, self=self)

        # Opens up a thread to handle connections
        Server.connectionsListener(self)

        # Reading command line inputs
        print("Type \"quit\" to quit at anytime")
        while True:
            if "quit" in input():
                sys.exit()
