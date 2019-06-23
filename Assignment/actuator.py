import time
import client


class Actuator():
    """Class to represent greenhouse's actuators.

    Open two channels of communication, one with Manager server to read
    instructions to be turned on and off, the other with Environment server to
    act on it.

    Parameters
    ----------
    `ID: str`
        Its identification and purpose, check it out on `Report.pdf`;

    `strength: float`
        Its strength of variation in the greenhouse;

    """

    def mana(self, client):
        """Receive orders from Manager.

        Protocols
        ---------

        `PUT <- MANA`
            Turns this actuator on or off;

        `ACK -> MANA`
            Confirms setting;

        """
        while True:
            data = None
            while not data:
                try:
                    data = client.sck.recv(1024)
                except Exception:
                    pass
            if client.v:
                print(client.ID + " <- " + client.target + ": " +
                      str(data, "utf-8"))
            data = str(data, "utf-8").split("|")
            if data[1] == "PUT" and data[2] == client.ID:
                if data[3] == "ON":
                    self.on[0] = True
                else:
                    self.on[0] = False
                # Acknowledgement
                string = "|ACK|PUT|"
                if client.v:
                    print(client.ID, "-> " + client.target + ": " + string)
                try:
                    client.sck.send(bytes(string, "utf-8"))
                except OSError:  # If connection error:
                    print(client.target + " disconnected")
                    print(client.ID + " disconnecting from " + client.target)
                    client.sck.close()
                    return

    def envi(self, client):
        """Interact with Environment.

        Protocols
        ---------

        `PUT -> ENVI`
            Acts on Environment;

        """
        while True:
            if self.on[0]:
                string = "|PUT|" + client.ID + "|" + str(self.strength) + "|"
                if client.v:
                    print(client.ID + " -> " + client.target + ": " + string)
                try:
                    client.sck.send(bytes(string, "utf-8"))
                except OSError:  # If connection error:
                    print(client.target + " disconnected")
                    print(client.ID + " disconnecting from " + client.target)
                    client.sck.close()
                    return
                time.sleep(1)

    def __init__(self, ID, strength):
        """Class constructor."""
        self.on = [False]
        self.strength = strength

        HOST, v = client.inputs()
        if HOST is not None:
            client.Client(7777, ID, "MANA", self.mana, v, HOST).start()
            client.Client(8888, ID, "ENVI", self.envi, v, HOST).start()
        else:
            client.Client(7777, ID, "MANA", self.mana, v).start()
            client.Client(8888, ID, "ENVI", self.envi, v).start()
