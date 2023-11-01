from socket import *
import os
import time
from datetime import datetime

def getLastModified(fileName):
    timeModified = os.path.getmtime(fileName)
    timeZoned = time.asctime(time.gmtime(timeModified))
    # print(timeModified)
    # print(timeZoned)
    # print(timeZoned.split())
    RFCFormat = timeZoned.split()[0] + ', ' + timeZoned.split()[2] + " " + timeZoned.split()[1] + " " + timeZoned.split()[4] + " " + timeZoned.split()[3] + " GMT"
    # print(RFCFormat)
    return RFCFormat

def getDate():
    # print("Curr gmt time")
    currGmt = time.gmtime()
    # print(currGmt)
    timeZoned = time.asctime(currGmt)
    RFCFormat = timeZoned.split()[0] + ', ' + timeZoned.split()[2] + " " + timeZoned.split()[1] + " " + timeZoned.split()[4] + " " + timeZoned.split()[3] + " GMT"
    # print(RFCFormat)
    return RFCFormat



serverIP = "127.0.0.1"
serverPort = 10500
serverSocket = socket(AF_INET, SOCK_STREAM) # welcoming socket
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    request = connectionSocket.recv(2048).decode()
    # print(type(request))
    fileName = request.partition('\n')[0].split()[1][1:]
    # print(fileName)
    response = ""
    if fileName != "HelloWorld.html":
        # 404
        response = "HTTP/1.1 404 Not Found\n\n File Not Found"
        print("File not found") # swap out for a 404 error msg
        connectionSocket.sendall(response.encode())
    else:
        print("sending file")
        file = open(fileName, 'r')
        fileData = file.read()
        file.close()
        # create headers
        # Connection 14.10?
        # Date 14.18
        # Server 14.38
        # Last-Modified 14.29
        # Content-Length 14.13
        # Content-Type 14.17
        statusMsg = "HTTP/1.1 200 OK\r\n"
        connection = "Connection: keep-alive\r\n"
        date ="Date: " + str(getDate()) + "\r\n" # Look at the RFC Format, the actual values needs to be preceded with name like:
        # Date: Tue, 15 Nov...
        server = "Server: Lab 2 Task 1; Python server\r\n"
        lastModified = "Last-Modified: " + str(getLastModified(fileName)) + "\r\n"
        
        contentLength = "Content-Length: " + str(len(fileData)) + "\r\n"
        contentType = "Content-Type: text/html\r\n\r\n"
        # headers =  + contentLength
        response = statusMsg + connection + date + server + lastModified + contentLength + contentType + fileData
        connectionSocket.sendall(response.encode())
        # connectionSocket.sendall(contentLength.encode())
        # connectionSocket.sendall(fileData.encode())
        # send response
        print("Done sending file")
    
        
    # sentence = connectionSocket.recv(2048).decode() # buffer size = 2048
    # capitalizedSentence = sentence.upper()
    # connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
    print('.')

