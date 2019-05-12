#REFERENCE
#https://en.wikibooks.org/wiki/Python_Programming/Threading
#https://docs.python.org/2/tutorial/classes.html
#https://docs.python.org/3/tutorial/modules.html
#https://wiki.python.org.br/SocketBasico
#https://www.geeksforgeeks.org/multithreading-in-python-set-2-synchronization/
#https://docs.python.org/3/library/socket.html

import socket
import threading
import serverthread

def closeserver():
    print "Type q to quit at anytime"
    while True:
        if ("q" in input()):
            tcp.close()
            quit()

threading.Thread(target=closeserver)

PORT = 7777

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((None, PORT))#'None' to accept any connection
tcp.listen()
#listen's arg is the max connections
#can be the number of sensors+actuators

while True:
    conn, addr = tcp.accept()
    serverthread(conn, adrr).start()

#lock = threading.Lock()
#lock.acquire()
#do stuff
#lock.release()
