from fileinput import filename
import socket

# localhost:8000/www.google.com
# localhost:8000/gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html

# Create socket and start lisetneing
portNumber = 8000
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind(('', portNumber))
serverSock.listen(1)

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    clientSock, address = serverSock.accept()
    print('Received a connection from:', address)
    sentence = clientSock.recv(2048)
    originURL = sentence.split()[1].decode()
    serverUrl = originURL[1:]
    cacheFileName = serverUrl.replace("www.", "", 1).replace("/", "_")
    fileName = serverUrl.replace("www.", "", 1).split('/')[0]
    path = serverUrl.partition("/")[2]
    fileExist = "false"

    try:
        # Checking the file exist in the cache
        f = open(cacheFileName, 'r')
        outputdata = f.readlines()
        for i in range(0, len(outputdata)):
            clientSock.send(outputdata[i].encode())
        clientSock.send("\r\n".encode())
        fileExist = "true"
        clientSock.send("HTTP/1.1 200 OK\r\n".encode())
        clientSock.send("Content-Type:text/html\r\n".encode())
        print('Read from cache!!\n')
        f.close()
    except FileNotFoundError:
        if fileExist == "false":
            # Create a socket interacting with URL server
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                ip = socket.gethostbyname(fileName)
                c.connect((ip, 80))
                print('Connected to ' + fileName)
                buffer = (
                    "GET /"+path + " HTTP/1.1\r\nHost:"+fileName+"\r\n\r\n")
                c.send(buffer.encode())
                recvData = c.recv(8192).decode()
                with open("./" + cacheFileName, "wb") as tmpFile:
                    for line in recvData:
                        tmpFile.write(line.encode())
                        clientSock.send(line.encode())

                print('Data sent to client!!\n\n')
                tmpFile.close()
                c.close()
            except IOError as e:
                ''
        else:
            # HTTP response data not found
            clientSock.send("HTTP/1.1 404 sendErrorErrorError\r\n")
            clientSock.send("Content-Type:text/html\r\n".encode())
            clientSock.send("\r\n".encode())

    clientSock.close()
serverSock.close()
