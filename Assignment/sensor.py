import time
import client


class Sensor():
    """Class to represent greenhouse's sensors.

    Open two channels of communication, one with Environment server to
    "measure" it, the other with Manager server to send him its measurements.

    Parameters
    ----------
    `ID: str`
        Its identification and purpose, check it out on `Report.pdf`;

    """

    def mana(self, client):
        """Send `PUT` command to Manager."""
        while self.info[0] is None:
            pass
        while True:
            string = "|PUT|" + client.ID + "|" + str(self.info[0]) + "|"
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

    def envi(self, client):
        """Receive `PUT` command from Environment. Store its data."""
        while True:
            data = None
            while not data:
                try:
                    data = client.sck.recv(1024)
                except Exception:
                    pass
            if client.v:
                print(client.ID + " <- " + client.target +
                      ": " + str(data, "utf-8"))
            data = str(data, "utf-8").split("|")
            if data[1] == "PUT" and data[2] == client.ID:
                self.info[0] = float(data[3])

    def __init__(self, ID):
        """Class constructor."""
        self.info = [None]

        HOST, v = client.inputs()
        if HOST is not None:
            client.Client(7777, ID, "MANA", self.mana, v, HOST).start()
            client.Client(8888, ID, "ENVI", self.envi, v, HOST).start()
        else:
            client.Client(7777, ID, "MANA", self.mana, v).start()
            client.Client(8888, ID, "ENVI", self.envi, v).start()
