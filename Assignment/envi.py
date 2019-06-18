
#!/usr/bin/python3

import server


def temp():
    print("yi from new temp")


def humi():
    print("yi from new humi")


functions = {
    "TEMP": temp,
    "HUMI": humi
}


def envi(serverThread):
    functions[serverThread.ID]()


if __name__ == "__main__":
    environment = server.Server(8888, "ENVI", envi)
