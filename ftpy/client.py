import socket
import os
from utils import *
 
PORT = int(input("Enter the port number.\n> "))
HOST = input("Enter IP address of the server.\n> ")

command = "pull"

def main():

	with socket.socket() as sock:
			sock.setblocking(True)
			sock.connect((HOST,PORT))
			print(f"[FTpy] Connected to {HOST}:{PORT}.")

			if command == "rls":
				header_sendall(sock,LS_MESSAGE.encode(FORMAT))
				file_list = header_recv(sock).decode().strip()
				print(file_list)
			elif command == "ls":
				pass
			elif command == "pull":
				header_sendall(sock,DOWNLOAD_MESSAGE.encode(FORMAT))
				header_sendall(sock,"hello.txt".encode(FORMAT))
				file_size = header_recv(sock).decode(FORMAT).strip()
				file_size = int(file_size)
				


			header_sendall(sock,DISCONNECT_MESSAGE.encode(FORMAT))
			sock.close()

if __name__ == "__main__":
	main()