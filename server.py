from socket import *
from utilities import *

# These are initialized for both server and client:
serverIP = "127.0.0.1"
serverPort = 10600 # different number here for testing

# Stored IP addresses, given in lab manual:
ip_addresses = {
    "google.com": {
        "Type": "A",
        "Class": "IN",
        "TTL": 260,
        "IP": ["192.165.1.1", "192.165.1.10"],
        "Sl": "1",
    },
    "youtube.com": {
        "Type": "A",
        "Class": "IN",
        "TTL": 160,
        "IP": ["192.165.1.2"],
        "Sl": "2",
    },
    "uwaterloo.ca": {
        "Type": "A",
        "Class": "IN",
        "TTL": 160,
        "IP": ["192.165.1.3"],
        "Sl": "3",
    },
    "wikipedia.org": {
        "Type": "A",
        "Class": "IN",
        "TTL": 160,
        "IP": ["192.165.1.4"],
        "Sl": "4",
    },
    "amazon.ca": {
        "Type": "A",
        "Class": "IN",
        "TTL": 160,
        "IP": ["192.165.1.5"],
        "Sl": "5",
    },
}

# Main function
def main():
    # Setup from tutorial example:
    serverSocket = socket(AF_INET, SOCK_DGRAM) # welcoming socket
    serverSocket.bind((serverIP, serverPort))
    # serverSocket.listen(1)
    print("The server is ready to receive")

    while True:
        # Receiving request:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode()
        formattedMessage = formatter(modifiedMessage)

        # Format and print the request:
        print("Received request:")
        print(formattedMessage)

        # Send the reply to the client:
        domain = getDomainFromRequest(modifiedMessage)
        requestID = modifiedMessage[:4]
        domainInfo = ip_addresses[domain]
        response = createDNS(domain, domainInfo, requestID)
        formattedReponse = formatter(response)

        print("Server response:")
        print(formattedReponse)

        # Send to the socket:
        serverSocket.sendto(response.encode(), clientAddress)

if __name__ == "__main__":
    main()