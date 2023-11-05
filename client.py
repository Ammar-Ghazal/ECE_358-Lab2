from socket import *
from utilities import *
from server import serverIP, serverPort
import re

def main():
    clientSocket = socket(AF_INET, SOCK_DGRAM) # welcoming socket
    # serverSocket.listen(1)
    # print("The server is ready to receive")

    while True:
        # Wait for user to input domain name, if user enters nothing, break the loop:
        if (userDomain := input("Enter Domain Name: ")).lower() == "exit": break

        # Convert user given domain to DNS request, and send to the server:
        toServer = createDNSHeader(userDomain)
        clientSocket.sendto(toServer.encode(), (serverIP, serverPort))

        # Get the response from the server and print it:
        serverResponse, addressUnused = clientSocket.recvfrom(2048)
        # - the unused address variable is here so that serverResponse is not 
        #   assigned the entire tuple, but only its part 
        printResponse(serverResponse.decode())
    
    # End connection to server:
    print("Session ended")
    clientSocket.close()

def printResponse(serverResponse):
    # First, get domain from the server response:
    domain = getDomainFromResponse(serverResponse)

    # Separate the domain into two pieces, discard everything before the name:
    resourceRecords = serverResponse.split('c00c')
    resourceRecords.pop(0) # discard

    # Once we have the name, use 4.5.3(lab manual) to assign values:
    for record in resourceRecords:
        # split components based on index of values
        indices = [0,4,8,12,16,24]
        # parts = [record[i:j] for i,j in zip(indices, indices[1:]+[None])]
        parts = []
        for start, end in zip(indices, indices[1:] + [None]):
            substring = record[start:end]
            parts.append(substring)

        # Fixed values:
        rType = "A"
        rClass = "IN"

        # Variable values:
        rTTL = int(parts[2], 16)
        rLength = int(parts[3], 16)
        rIPAddress = hexToIP(parts[4])

        # Print to console:
        print("> {}: type {}, class {}, TTL {}, addr ({}) {}".format(domain,rType,rClass,rTTL,rLength,rIPAddress))

def hexToIP(msg):
    # Sepearate the input into "octets" and convert them to decimal
    octets = [int(msg[i:i+2], 16) for i in range(0, len(msg), 2)]

    # Concatenate them to form an IP address X.X.X.X
    return '.'.join(map(str, octets))

if __name__ == "__main__":
    main()
