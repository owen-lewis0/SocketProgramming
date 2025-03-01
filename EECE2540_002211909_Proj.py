"""
Owen Lewis, NUID: 002211909

I started my code by connecting creating the client socket and connecting it to the remote server. The socket library makes this
fairly straight forward, I just had to get the IP address and acceptable port numbers from Canvas. Once the server was connected,
I needed to send the designated intro message. This is when I started my loop. I could've used a for-loop that would go through
exactly 100 expressions and the necessary success message, but I just did an infinite loop that breaks when the flag is sent.
Inside the loop we recieve the encoded message from the server and decode it and split it's parts into an array to manage the 
expressions. There are the if-else statements set up for the following cases: Success, failure, and EXPR(expressions). The success
and failure cases both end the program and print out their statuses, but the success case also prints the secret flag. The expression
case has four if statements inside it, one for each operator (+, -, *, /). Each of these, if true, calls the two number associated with
the message and executes the operation. This message is then encoded and sent back to the server to be checked. Lastly, after the loop
is broken, the client socket is close and the program finishes.

I tested my code using the sample server first. Once I was sure that my program was properly evaluating the expressions,
I switched over to the remote server. At first I couldn't connect to hte server using port 12000, but it immediately
connected when I switched to port 12001. My first error that I was stuck on for a while was saying that AF_INET and SOCK_STREAM 
weren't defined. This was eventually fixed by changing "import socket" to "from socket import *". Another issue I was having was
with splitting the string, which I tried to make a separate function for at first. I then realized that the remote server was
processing my messages similarly, so I looked through the sample server code and found that it used the split() function, which
made my code much simpler.

Secret flag: c74b9d42865f495114dea52c5f53966824eac33de6a479320659292fec478f37
"""
from socket import *

#IP address and port number
ipAddress = "129.10.33.215"
portNumber = 12001 #12000 wouldn't connect, switched to 12001
serverIdentifier = (ipAddress ,portNumber )

#Creating a socket
clientSocket = socket(AF_INET, SOCK_STREAM)

#Establishing a connection
clientSocket.connect(serverIdentifier)

intro = 'EECE2540 INTR 002211909'
intro = intro.encode()
clientSocket.send(intro)

#Will run for all 100 expressions,
#loop breaks when success/failure message is recieved
while True:
	#Receiving a message
	serverRecieve = clientSocket.recv(4096) #4096 is buffer size
	#Get string version of message
	expr = serverRecieve.decode()
	print(expr)
	
	#Make array of each part of the string between spaces
	messageArr = expr.split()

	#Element of index 1 is the second section of message
	#The EECE2540 part is redundant
	
	#Case for success
	if messageArr[1] == "SUCC":
		Secret = messageArr[2] 
		print ("Success")		
		print(Secret)	
		break

	#Case for failure
	elif messageArr[1] == "FAIL":
		print("Failed: Wrong Answer")
		break


	#Case for expression
	#Array indices 2 and 4 are operands, index 3 is operator
	elif messageArr[1] == "EXPR":
		if messageArr[3] == "+":
			ans = int(messageArr[2]) + int(messageArr[4])
		elif messageArr[3] == "-":
			ans = int(messageArr[2]) - int(messageArr[4])
		elif messageArr[3] == "*":
			ans = int(messageArr[2]) * int(messageArr[4])
		elif messageArr[3] == "/":
			ans = int(messageArr[2]) / int(messageArr[4])
		out = "EECE2540 RSLT "+str(ans) #Result message sent back to server
		print(out)
		
		#sending our result
		out = out.encode()
		clientSocket.send(out)
	else:
		break

# Closing the socket
clientSocket.close()

print("Finished")