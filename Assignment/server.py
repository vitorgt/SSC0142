import sys
import atexit
import socket
import threading


def threaded(fn):
    """Wrap any function as a new thread."""
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args,
                         kwargs=kwargs, daemon=True).start()
    return wrapper


class ServerThread(threading.Thread):
    """Handle each new connection with server making it a new thread.

    Attributes
    ----------
    `server: Server`
        A reference to access attributes on Server;

    `conn: Socket`
        Connection to socket;

    `addr: IP address`
        Socket's IP;

    `ID: str`
        Connector's identification and purpose, check it out on `Report.pdf`;

    Raises
    ------
    `ConnectionRefusedError`
        If protocols received out of sync or unknown protocol received;

    """

    def __init__(self, server, conn, addr):
        """Class constructor."""
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
        """Attempt to close the connection and kill thread."""
        print("Closing connection with", self.addr)
        self.conn.close()
        sys.exit()

    def run(self):
        """Thread main function."""
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
                print(self.server.ID + " -> " + self.ID + ": " + string)
            try:
                self.conn.send(bytes(string, "utf-8"))
            except OSError:  # If connection error:
                print(self.ID + " disconnected")
                print(self.server.ID + " disconnecting from " + self.ID)
                self.conn.close()
                sys.exit()
        else:
            raise ConnectionRefusedError("unknown protocol received")

        # Runs server specific function
        self.server.fn(self)


class Server:
    """Open a socket.

    Attributes
    ----------
    `PORT: int`
        Port in which socket will be opened;

    `ID: str`
        Server's identification and purpose, check it out on `Report.pdf`;

    `fn: function`
        Function that will be executed at port;

    """

    @threaded
    def connectionsListener(self):
        """Listen to the port waiting for new connections opening threads."""
        while True:
            conn, addr = self.server.accept()
            conn.settimeout(3.0)
            ServerThread(server=self, conn=conn, addr=addr).start()

    def closeServer(self):
        """Attempt to close socket."""
        try:
            self.server.close()
        except Exception as e:
            print("Server could not be closed because of", e)
            print("Closing application anyway")
        else:
            print("Server successfully closed")

    def __init__(self, PORT, ID, fn):
        """Class constructor."""
        self.PORT = PORT
        self.ID = ID
        self.fn = fn
        self.v = True

        # Reading command line inputs
        # "-v" to deactivate verbose mode
        for x in range(len(sys.argv)):
            if "-v" in sys.argv[x]:
                self.v = False

        # Opens socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', self.PORT))  # '' to accept any connection
        self.server.listen()

        # When exiting application, close server
        atexit.register(Server.closeServer, self=self)

        # Function to handle connections
        Server.connectionsListener(self)

        # Reading command line inputs
        print("Type \"quit\" to quit at anytime")
        print("Type \"v\" to toggle verbose mode at anytime")
        while True:
            if "quit" in input():
                sys.exit()
            if "v" in input():
                self.v = not self.v
