import sys
import atexit
import socket
import threading


def threaded(fn):
    """Wrapper that makes any function a new thread"""
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args,
                         kwargs=kwargs, daemon=True).start()
    return wrapper


class ServerThread(threading.Thread):
    """
    Class that handles each new connection with server making it a new thread

    Attributes
    ----------
    server : Server object
        A reference to acess atributes on Server;
    conn : Socket
        Connection to socket;
    addr : IP address
        IP's connection to socket;
    ID : str
        Connector's ID;

    Raises
    ------
    ConnectionRefusedError
        If protocols received out of sync or unknown protocol received
    """

    def __init__(self, server, conn, addr):

        self.server = server
        self.conn = conn
        self.addr = addr[0]
        self.ID = None
        print("New connection with", self.addr)

        # When exiting application, close connection
        atexit.register(ServerThread.closeConn, self=self)

        # Starts running the thread
        threading.Thread.__init__(self)

    def closeConn(self):
        """Attempts to close the connection and kill thread"""
        print("Closing connection with", self.addr)
        self.conn.close()
        sys.exit()

    def run(self):

        # Receives connection
        data = None
        while not data:
            try:
                data = self.conn.recv(1024)
            except Exception:
                pass
        if self.server.v:
            print(self.server.ID, "<-:", str(data, "utf-8"))
        data = str(data, "utf-8").split("|")

        # Acknowledgement
        if "CON" == data[1]:
            self.ID = data[2]
            string = "|ACK|CON|"
            if self.server.v:
                print(self.server.ID+" -> "+self.ID+": "+string)
            try:
                self.conn.send(bytes(string, "utf-8"))
            except OSError:
                print(self.ID+" disconnected")
                print(self.server.ID+" disconnecting from "+self.ID)
                self.conn.close()
                sys.exit()
        else:
            raise ConnectionRefusedError("unknown protocol received")

        # Runs server specific function
        self.server.fn(self)


class Server:

    @threaded
    def connectionsListener(self):
        while True:
            conn, addr = self.server.accept()
            conn.settimeout(3.0)
            ServerThread(server=self, conn=conn, addr=addr).start()

    # Attempts to close server
    def closeServer(self):
        try:
            self.server.close()
        except Exception as e:
            print("Server could not be closed because of", e)
            print("Closing application anyway")
        else:
            print("Server successfully closed")

    def __init__(self, PORT, ID, fn):

        self.PORT = PORT
        self.ID = ID
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
        print("Type \"v\" to toggle verbose mode at anytime")
        while True:
            if "quit" in input():
                sys.exit()
            if "v" in input():
                self.v = not self.v
