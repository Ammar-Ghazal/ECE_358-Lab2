from socket import *
import os
import time
from datetime import datetime

def getLastModified(fileName):
    timeModified = os.path.getmtime(fileName)
    timeZoned = time.asctime(time.gmtime(timeModified))

    RFCFormat = timeZoned.split()[0] + ', ' + timeZoned.split()[2] + " " + timeZoned.split()[1] + " " + timeZoned.split()[4] + " " + timeZoned.split()[3] + " GMT"
   
    return RFCFormat

def getDate():
    
    currGmt = time.gmtime()
    
    timeZoned = time.asctime(currGmt)
    RFCFormat = timeZoned.split()[0] + ', ' + timeZoned.split()[2] + " " + timeZoned.split()[1] + " " + timeZoned.split()[4] + " " + timeZoned.split()[3] + " GMT"
    
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

    fileName = request.partition('\n')[0].split()[1][1:]
    
    response = ""
    statusMsg = ""
    connection = ""
    date = ""
    server = ""
    lastModified = ""
    contentLength = ""
    contentType = ""

    
    try:
        file = open(fileName, 'r')
        print("Starting to send file")
        fileData = file.read()
        file.close()

        # Connection 14.10
        # Date 14.18
        # Server 14.38
        # Last-Modified 14.29
        # Content-Length 14.13
        # Content-Type 14.17
        isHead = False
        requestType = request.partition('\n')[0].split()[0]
        if requestType == 'HEAD':
            isHead = True

        statusMsg = "HTTP/1.1 200 OK\r\n"
        connection = "Connection: keep-alive\r\n"
        date ="Date: " + str(getDate()) + "\r\n" 
        server = "Server: Lab 2 Task 1; Python server\r\n"
        lastModified = "Last-Modified: " + str(getLastModified(fileName)) + "\r\n"
        
        contentLength = "Content-Length: " + str(len(fileData)) + "\r\n"
        contentType = "Content-Type: text/html\r\n\r\n"

        response = statusMsg + connection + date + server + lastModified

        if isHead:
            contentLength = "Content-Length: " + str(0) + "\r\n"
        response = response + contentLength + contentType
        if not isHead:
            response = response + fileData
        connectionSocket.sendall(response.encode())
        print("Done sending file")
    except FileNotFoundError:
        # 404
        statusMsg = "HTTP/1.1 404 Not Found\r\n"
        connection = "Connection: keep-alive\r\n"
        date ="Date: " + str(getDate()) + "\r\n" 
        server = "Server: Lab 2 Task 1; Python server\r\n"
        lastModified = "Last-Modified: " + "Not Applicable" + "\r\n"
        
        contentLength = "Content-Length: " + str(0) + "\r\n"
        contentType = "Content-Type: Not Applicable\r\n\r\n"
        
        response = statusMsg + connection + date + server + lastModified
        
        response = response + contentLength + contentType
        
        connectionSocket.sendall(response.encode())
        
    
    connectionSocket.close()

