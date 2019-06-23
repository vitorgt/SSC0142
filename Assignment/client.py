import sys
import socket
import threading


def inputs():
    """Read command line inputs.

    `-ip X.X.X.X` to set server's IP address

    `-v` to deactivate verbose mode

    """
    HOST = None
    v = True
    for x in range(len(sys.argv)):
        if "-ip" in sys.argv[x]:
            HOST = sys.argv[x + 1]
        if "-v" in sys.argv[x]:
            v = False
    return HOST, v


class Client(threading.Thread):
    """Handle each new connection with server making it a new thread.

    Attributes
    ----------
    `PORT: int`
        Server's port to connect socket;

    `ID: str`
        Client's identification and purpose, check it out on `Report.pdf`;

    `target: str`
        Server's identification and purpose, check it out on `Report.pdf`;

    `fn: function`
        Function that will be executed by client at connection;

    `v: bool`
        Shows all messages executed by the program on terminal (`verbose`);

    `HOST: IP address`
        Server's IP (default = `127.0.0.1` a.k.a. `localhost`);

    `sck: socket`
        Socket channel;

    Protocols
    ---------
    `CON -> Server`
        Asks for connection with servers, i.e. Manager and Environment;

    `ACK <- Server`
        Gets connection acknowledgement;

    Raises
    ------
    `ConnectionRefusedError`
        If protocols received out of sync or unknown protocol received;

    """

    def __init__(self, PORT, ID, target, fn, v=True, HOST="127.0.0.1"):
        """Class constructor."""
        self.PORT = PORT
        self.ID = ID
        self.target = target
        self.fn = fn
        self.v = v
        self.HOST = HOST
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sck.settimeout(3.0)
        threading.Thread.__init__(self)

    def run(self):
        """Thread main function."""
        # Connection
        showed = False
        while True:
            try:
                self.sck.connect((self.HOST, self.PORT))
            except ConnectionRefusedError:
                if not showed and self.v:
                    print(self.target, "is not online, trying again")
                    showed = True
            else:
                if self.v:
                    print(self.target, "is online, attempting to connect")
                break

        # Identification
        if self.v:
            print(self.ID + " -> " + self.target + ": |CON|" + self.ID + "|")
        try:
            self.sck.send(bytes("|CON|" + self.ID + "|", "utf-8"))
        except OSError:  # If connection error:
            print(self.target + " disconnected")
            print(self.ID + " disconnecting from " + self.target)
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
            print(self.ID + " <- " + self.target + ":", str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if data[1] == "ACK" and data[2] == "CON":
            # Running client specific function
            self.fn(self)
        else:
            self.sck.close()
            raise ConnectionRefusedError("unknown protocol received")
