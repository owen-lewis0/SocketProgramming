##################################################################################################
# This program is a sample server for the socket programming assignment. It generates a set of    				       	#
# simple mathematical expressions as strings, which are sent via TCP to the client. The client    					#
# needs to send back the correct answer for each of the operations. When enough correct results   					#
# have been received, a secret flag is generated and sent back to the client. Finally, the        						#
# connection is closed, and the server proceeds to shut down.                                     							#
#                                                                                                 												#
# This program was initially authored by Carlos Bocanegra <bocanegrac@coe.neu.edu>.               					#
# It has since been edited by Kevin Hines <hines.ke@husky.neu.edu> and Abhimanyu Venkatraman      				#
# Sheshashayee <abhi.vs@outlook.com>.                                                             								#
##################################################################################################

# Imports
import hashlib
import random
import socket
import sys

# Constants
SERVER_HOSTNAME = 'localhost'
DEFAULT_SERVER_PORT = 12000
BUFFER_SIZE = 4096
NUMBER_OF_EXPRESSIONS = 100
SECRET_KEY = "This sample key is secret".encode()

# Functions
def generate_secret_flag(NU_ID):
    """Generate a secret given a NU ID number and a secret key."""
    return hashlib.sha256(SECRET_KEY + NU_ID.encode()).hexdigest()

def generate_maths():
    """Generate random mathematical expressions in the format 'n1 op n2'."""
    operations = ['+', '-', '*', '/']
    op = random.choice(operations)
    left_value = random.randint(1, 1000)
    right_value = random.randint(1, 1000)

    expression = f"{left_value} {op} {right_value}"
    
    if op == '+':
        solution = left_value + right_value
    elif op == '-':
        solution = left_value - right_value
    elif op == '*':
        solution = left_value * right_value
    elif op == '/':
        solution = left_value / right_value

    return expression, solution

def run_server(server_port):
    """Set up the server, handle incoming client communications."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOSTNAME, server_port))
    server_socket.listen(5)
    print("Server ready to accept connections. Waiting...")

    connection_socket, address = server_socket.accept()
    print(f"Connection established | Hostname: {address[0]} | Port: {address[1]}")

    try:
        message_from_client = connection_socket.recv(BUFFER_SIZE).decode('utf-8')
    except Exception as e:
        print(f"Error: unable to receive message from client. | {e}")
        return

    if message_from_client:
        tokens = message_from_client.split()
        if tokens[0] == "EECE2540" and tokens[1] == "INTR":
            NU_ID = tokens[2]
            secret_flag = generate_secret_flag(NU_ID)

            for _ in range(NUMBER_OF_EXPRESSIONS):
                expression, solution = generate_maths()
                message_to_client = f"EECE2540 EXPR {expression}"

                try:
                    connection_socket.send(message_to_client.encode('utf-8'))
                except:
                    print(f"Error: unable to send message to client. | {message_to_client}")
                    break

                try:
                    message_from_client = connection_socket.recv(BUFFER_SIZE).decode('utf-8')
                except:
                    print("Error: unable to receive message from client.")
                    break

                if message_from_client:
                    tokens = message_from_client.split()
                    if tokens[0] == "EECE2540" and tokens[1] == "RSLT":
                        received_result = tokens[2]
                        if str(solution) != received_result:
                            print(f"Error: incorrect result. | Expected: {solution} | Received: {received_result}")
                            connection_socket.send("EECE2540 FAIL".encode('utf-8'))
                            break
                    else:
                        print(f"Error: invalid message type. | {message_from_client}")
                        connection_socket.send("EECE2540 FAIL".encode('utf-8'))
                        break
                else:
                    connection_socket.send("EECE2540 FAIL".encode('utf-8'))
                    break
            else:
                print(f"Success! | {NU_ID} -> {secret_flag}")
                connection_socket.send(f"EECE2540 SUCC {secret_flag}".encode('utf-8'))
        else:
            print(f"Error: invalid initial message format. | {message_from_client}")
            connection_socket.send("EECE2540 FAIL".encode('utf-8'))
    else:
        print("Error: empty message from client.")
        connection_socket.send("EECE2540 FAIL".encode('utf-8'))

    connection_socket.close()
    print(f"Connection closed. | Hostname: {address[0]} | Port: {address[1]}")
    server_socket.close()
    print("Server terminating...")

# Entry point
if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_server(int(sys.argv[1]))
    else:
        run_server(DEFAULT_SERVER_PORT)