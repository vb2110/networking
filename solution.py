#import socket module
from socket import *
import sys # In order to terminate the program
def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    while True:
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  #Fill in start      #Fill in end
        try:
            message = connectionSocket.recv(4096)
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read() # reads the file contents Fill in start     #Fill in end
            connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            connectionSocket.send('\nHTTP/1.1 404 Not Found\r\n\r\n'.encode('utf-8'))
            connectionSocket.close()
    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data
if __name__ == "__main__":
    webServer(13331)
