from socket import *

serverPort = 8888
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to recieve')
while True:
    clientSocket, addr = serverSocket.accept()
    print(f"connection {addr} has established")
    try:
        sentence = clientSocket.recv(1024)
        filename = sentence.split()[1]
        File = open(filename[1:])
        output = File.read()
        clientSocket.send('HTTP/1.1 200 OK\n\n'.encode())
        for i in range(0, len(output)):
            clientSocket.send(output[i].encode())
        clientSocket.send("\r\n".encode())
        print('Output data sent to client!\n')
        clientSocket.close()
    except IOError:
        clientSocket.send("\nHTTP/1.1 404 Not Found\n\n".encode())
        clientSocket.close()
# localhost:8888/HelloWorld.html
