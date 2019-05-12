#REFERENCE
#

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
tcp.bind((None, PORT))
tcp.listen()#can be the number of sensors+actuators

while True:
    conn, addr = tcp.accept()
    threading.Thread(target=serverthread, args=(conn, addr,)).start()

#lock = threading.Lock()
#lock.acquire()
#do stuff
#lock.release()
