from socket import *
import os
import time
from datetime import datetime

# helper function for Last-Modified field in response header
def getLastModified(fileName):
    timeModified = os.path.getmtime(fileName)
    timeZoned = time.asctime(time.gmtime(timeModified))
    RFCFormat = timeZoned.split()[0] + ', ' + timeZoned.split()[2] + " " + timeZoned.split()[1] + " " + timeZoned.split()[4] + " " + timeZoned.split()[3] + " GMT"
   
    return RFCFormat
# helper function for Date field in response header
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
    
    # Try-Except to find requested file.  If found then file data used in response.  If not, 404 response returned
    try:
        file = open(fileName, 'r')
        print("Starting to send file")
        fileData = file.read()
        file.close()
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
        responseBody = "404 Not Found"
        # print(len(responseBody))
        statusMsg = "HTTP/1.1 404 Not Found\r\n"
        connection = "Connection: keep-alive\r\n"
        date ="Date: " + str(getDate()) + "\r\n" 
        server = "Server: Lab 2 Task 1; Python server\r\n"
        lastModified = "Last-Modified: " + "Not Applicable" + "\r\n"
        contentLength = "Content-Length: " + str(len(responseBody)+1) + "\r\n"
        contentType = "Content-Type: text/html\r\n\r\n\n"
        
        response = statusMsg + connection + date + server + lastModified
        response = response + contentLength + contentType
        response = response + responseBody
        connectionSocket.sendall(response.encode())
        
    
    connectionSocket.close()

