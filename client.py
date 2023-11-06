from socket import *
from utilities import *
from server import serverIP, serverPort

def main():
    clientSocket = socket(AF_INET, SOCK_DGRAM) # welcoming socket
    # serverSocket.listen(1)
    # print("The server is ready to receive")

    while True:
        # Wait for user to input domain name, if user enters nothing, break the loop:
        if (userDomain := input("Enter Domain Name: ")).lower() == "exit": break

        # Convert user given domain to DNS request, and send to the server:
        toServer = createDNS(userDomain)
        clientSocket.sendto(toServer.encode(), (serverIP, serverPort))

        # Get the response from the server and print it:
        serverResponse, addressUnused = clientSocket.recvfrom(2048)
        # - the unused address variable is here so that serverResponse is not 
        #   assigned the entire tuple, but only its part 
        printResponse(serverResponse.decode())
    
    # End connection to server:
    print("Session ended")
    clientSocket.close()

if __name__ == "__main__":
    main()
