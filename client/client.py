import socket
import os
from futils import *
 
PORT = int(input("Enter the port number.\n> "))
HOST = input("Enter IP address of the server.\n> ")

try:
	with socket.socket() as sock:
		sock.setblocking(True)
		sock.connect((HOST,PORT))
		print(f"[FTpy] Connected to {HOST}:{PORT}.")

		header_sendall(sock,DISCONNECT_MESSAGE.encode())
		sock.close()
finally:
	sock.close()