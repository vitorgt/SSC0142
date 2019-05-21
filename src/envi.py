#!/usr/bin/python3

import sys
import atexit
import socket
import threading
import envi_thread


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True  # to kill the thread when closing the program
        thread.start()
    return wrapper


class Environment:

    @threaded
    def connectionslistener(self):
        while True:
            conn, addr = self.server.accept()
            envi_thread.EnviThread(manager=self, conn=conn).start()

    def closeserver(self):
        try:
            self.server.close()
        except Exception as e:
            print("Environment's server could not be closed because of", e)
            print("Closing application anyway")
        else:
            print("Environment's server successfully closed")

    def __init__(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 7777))  # '' to accept any connection
        self.server.listen()

        # when exiting application, close server
        atexit.register(Environment.closeserver, self=self)

        Environment.connectionslistener(self)


if __name__ == "__main__":
    Environment()
