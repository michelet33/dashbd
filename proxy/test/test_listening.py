import sys
import socket
import select
import threading
import sys

TCP_IP = '192.168.1.129'
TCP_PORT = 9001
BUFFER_SIZE = 2048
targetHost = "127.0.0.1"
targetPort = 9010
param = []

terminateAll = False


class ClientThread(threading.Thread):
    def __init__(self, clientSocket, targetHost, targetPort):
        threading.Thread.__init__(self)
        self.__clientSocket = clientSocket
        self.__targetHost = targetHost
        self.__targetPort = targetPort

    def run(self):
        print
        "Client Thread started"

        self.__clientSocket.setblocking(0)

        targetHostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        targetHostSocket.connect((self.__targetHost, self.__targetPort))
        targetHostSocket.setblocking(0)

        clientData = ""
        targetHostData = ""
        terminate = False
        while not terminate and not terminateAll:
            inputs = [self.__clientSocket, targetHostSocket]
            outputs = []

            if len(clientData) > 0:
                outputs.append(self.__clientSocket)

            if len(targetHostData) > 0:
                outputs.append(targetHostSocket)

            try:
                inputsReady, outputsReady, errorsReady = select.select(inputs, outputs, [], 1.0)
            except Exception:
                print("Exception ClientThread")
                break

            for inp in inputsReady:
                if inp == self.__clientSocket:
                    try:
                        data = self.__clientSocket.recv(4096)
                    except Exception:
                        print("Exception ClientThread")

                    if data is not None:
                        if len(data) > 0:
                            targetHostData += data
                        else:
                            terminate = True
                elif inp == targetHostSocket:
                    try:
                        data = targetHostSocket.recv(4096)
                    except Exception:
                        print("Exception ClientThread")

                    if data is not None:
                        if len(data) > 0:
                            clientData += data
                        else:
                            terminate = True

            for out in outputsReady:
                if out == self.__clientSocket and len(clientData) > 0:
                    bytesWritten = self.__clientSocket.send(clientData)
                    if bytesWritten > 0:
                        clientData = clientData[bytesWritten:]
                elif out == targetHostSocket and len(targetHostData) > 0:
                    bytesWritten = targetHostSocket.send(targetHostData)
                    if bytesWritten > 0:
                        targetHostData = targetHostData[bytesWritten:]

        self.__clientSocket.close()
        targetHostSocket.close()
        print("ClientThread terminating")



print('Listening for client...')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP,TCP_PORT))
server.listen(1)
rxset = [server]
txset = []


while 1:
    rxfds, txfds, exfds = select.select(rxset, txset, rxset)
    for sock in rxfds:
        if sock is server:
            conn, addr = server.accept()
            conn.setblocking(0)
            rxset.append(conn)
            print('Connection from address:', addr)
            ClientThread(conn, targetHost, targetPort).start()
        else:
            try:
                data = sock.recv(BUFFER_SIZE)
                print(data)
                if data == ";" :
                    print("Received all the data")
                    for x in param:
                        print(x)
                    rxset.remove(sock)
                    sock.close()
                else:
                    if str(data) != '':
                        print("received data: ", data)
            except Exception:
                print("Connection closed by remote end")
                param = []
                rxset.remove(sock)
                sock.close()
