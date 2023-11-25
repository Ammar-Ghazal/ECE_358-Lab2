# Lab 2

*** In Collaboration with Mark Kolodziej ***

## Task 1

To start the webserver for task 1 run
```bash
make task1
```
The console prints
```bash
The server is ready to receive 
```
The requested file can then be viewed on a web browser.

N.B. For 404 responses Date-Modified is 'Not Applicable', Content-Type is text/html to render the 404 message, and Content-Length is the length of the 404 message.  
## Task 2

Start with opening two different console windows, both must be at the same directory where server.py, client.py, and utilities.py all reside.

On one console, run the server by entering:
```bash
python server.py
```
Once the server is up, you should see this:
```bash
The server is ready to receive
```

On the other console, run the client by entering:
```bash
python client.py
```
Once the client is running, you should see the following prompt:
```bash
Enter Domain Name: 
```

Now, on the client console, you can request one of the 5 URLs:
1. google.com
2. youtube.com
3. uwaterloo.ca
4. wikipedia.org
5. amazon.ca

Once you enter one of the above URLs, you should see something like this on the server console:
```bash
The server is ready to receive
Received request:
24 bd 00 80 00 01 00 00 00 00 00 00 06 67 6f 6f 67 6c 65 03 63 6f 6d 00 00 01 00 01
Server response:
24 bd 10 80 00 01 00 02 00 00 00 00 06 67 6f 6f 67 6c 65 03 63 6f 6d 00 00 01 00 01 c0 0c 00 01 00 01 01 04 00 04 c0 a5 01 01 c0 0c 00 01 00 01 01 04 00 04 c0 a5 01 0a
```
And this on your client console:
```bash
Enter Domain Name: google.com
> google.com: type A, class IN, TTL 260, addr (4) 192.165.1.1
> google.com: type A, class IN, TTL 260, addr (4) 192.165.1.10
Enter Domain Name: 
```

Then, on the client console, you can type any other URL once you get a response.

Once you are done, type: "exit" and press enter on the client console.
```bash
Enter Domain Name: exit
Session ended
```
