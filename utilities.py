# Imports:
import random

######################## HELPER FUNCTIONS ########################
def formatter(initial):
    """ 
        Groups things in twos for formatting:
    """
    formatted = ""
    for i in range(0, len(initial), 2):
        formatted += initial[i:i+2] + " "
    formatted = formatted.rstrip()
    return formatted

def getDomainFromRequest(request):
    # Initialize variables:
    allDomainParts = []
    index = 24  # Header is 24 bits long, we don't care about it

    # Iterate through the whole request:
    while index < len(request):
        # This is the length of the domain part that we are currently reading:
        lengthOfPart = int(request[index:index + 2], 16)

        # If the length of the part is 0, it means we reached the end of the domain name:
        if lengthOfPart == 0:
            break

        # Read a domain part from the request and add it to allDomainParts
        domainPart = bytes.fromhex(request[index + 2:index + 2 + (lengthOfPart * 2)]).decode('utf-8')
        allDomainParts.append(domainPart)
        index += (2 + (lengthOfPart * 2))

    return '.'.join(allDomainParts)

def createDNS(domain, response=None, id=None):
    ################## DNS HEADER GENERATION START ##################
    # Generate a random ID and turn it to hex format, assign all flags:
    id = hex(int(randomID(), 2))[2:] if id is None else id
    
    qr = '0' if response is None else '1'
    opCode = '0'    # fixed value
    aa = '1'        # fixed value
    tc = '0'        # fixed value
    rd = '0'        # fixed value
    ra = '0'        # fixed value
    z = '000'       # fixed value
    rCode = '0'     # fixed value
    qdCount = "{:04x}".format(1)
    anCount = "{:04x}".format(0) if response is None else "{:04x}".format(len(response['IP']))
    nsCount = "{:04x}".format(0)
    arCount = "{:04x}".format(0)
    flags = "{:04x}".format(int(qr+opCode+aa+tc+rd+ra+z+rCode, 2))
    ################### DNS HEADER GENERATION END ###################

    ################### QUESTION GENERATION START ###################
    # Generate qName, qType, and qClass:
    subDomain = domain.split('.')[0]
    topDomain = domain.split('.')[1]
    subEncoded = subDomain.encode().hex()
    topEncoded = topDomain.encode().hex()
    qName = "{:02x}".format(len(subDomain)) + subEncoded + "{:02x}".format(len(topDomain)) + topEncoded + "{:02x}".format(0)
    # qName = f"{len(subDomain):02x}{subEncoded}{len(topDomain):02x}{topEncoded}00"
    qType = "{:04x}".format(1)
    qClass = "{:04x}".format(1)
    #################### QUESTION GENERATION END ####################

    #################### ANSWER GENERATION START ####################
    answer = ''
    if response is not None:
        # Must check every IP address to generate answer:
        for currentIP in response['IP']:
            # Assign variables:
            aName = 'c00c'
            aType = "{:04x}".format(1)
            aClass = "{:04x}".format(1) # according to documentation, 0x0001 is used for 'IN'
            aTTL = "{:04x}".format(response['TTL']) # get TTL values from the ip_addresses -- debug try :08
            aRDLength = "{:04x}".format(4)

            # Get the IP address and turn it to hex:
            ipHex = ''.join(["{:02x}".format(int(num)) for num in currentIP.split('.')])
            # print(ipHex)
            # print("IP IN HEX^")

            # Increment answer accumulator:        
            answer += aName + aType + aClass + aTTL + aRDLength + ipHex
    ##################### ANSWER GENERATION END #####################

    # Add all of the values to the newResponse variable and return it:
    newResponse = id + flags + qdCount + anCount + nsCount + arCount + qName + qType + qClass + answer
    return newResponse

# Generates a random 16 bit address in binary:
def randomID():
    return ''.join(str(random.randint(0, 1)) for _ in range(16))

def hexToIP(msg):
    # Sepearate the input into "octets" and convert them to decimal
    octets = [int(msg[i:i+2], 16) for i in range(0, len(msg), 2)]

    # Concatenate them to form an IP address X.X.X.X
    return '.'.join(map(str, octets))

def printResponse(serverResponse):
    # First, get domain from the server response:
    domain = getDomainFromRequest(serverResponse)

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

# # Taken from dnslib, DNSRecord: -- not used
# def parse(cls,packet):
        # """
        #     Parse DNS packet data and return DNSRecord instance
        #     Recursively parses sections (calling appropriate parse method)
        # """
        # buffer = DNSBuffer(packet)
        # try:
        #     header = DNSHeader.parse(buffer)
        #     questions = []
        #     rr = []
        #     auth = []
        #     ar = []
        #     for i in range(header.q):
        #         questions.append(DNSQuestion.parse(buffer))
        #     for i in range(header.a):
        #         rr.append(RR.parse(buffer))
        #     for i in range(header.auth):
        #         auth.append(RR.parse(buffer))
        #     for i in range(header.ar):
        #         ar.append(RR.parse(buffer))
        #     return cls(header,questions,rr,auth=auth,ar=ar)
        # except DNSError:
        #     raise
        # except (BufferError,BimapError) as e:
        #     raise DNSError("Error unpacking DNSRecord [offset=%d]: %s" % (
        #                             buffer.offset,e))