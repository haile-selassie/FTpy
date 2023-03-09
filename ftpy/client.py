import socket
import os
from utils import *
import re
 
PORT = int(input("Enter the port number.\n> "))
HOST = input("Enter IP address of the server.\n> ")

def main():
	with socket.socket() as sock:
			sock.setblocking(True)
			sock.connect((HOST,PORT))
			print(f"[FTpy] Connected to {HOST}:{PORT}.")

			while True:
				choice = input("FTpy> ").split()
				command = choice[0]
				if command == "rls":
					header_sendall(sock,LS_MESSAGE.encode(FORMAT))
					file_list = header_recv(sock).decode().strip()
					print(file_list)
				elif command == "ls":
					file_list = "\n".join([file for file in os.listdir()])
					print(file_list)
				elif command == "download":
					filename = choice[1]
					header_sendall(sock,DOWNLOAD_MESSAGE.encode(FORMAT))
					header_sendall(sock,filename.encode(FORMAT))
					file_size = header_recv(sock).decode(FORMAT).strip()
					file_size = int(file_size)
					if file_size == 0:
						print(f"[FTpy] ERROR: {filename} does not exist.")
						continue
					with open(filename,"wb") as newfile:
						left = file_size
						while left > 0:
							if left < BUFFER_SIZE:
								newfile.write(sock.recv(left))
								left = 0
							else:
								newfile.write(sock.recv(BUFFER_SIZE))
								left-=BUFFER_SIZE
					print(f"[FTpy] Downloaded {filename} from {HOST}")
				elif command == "upload":
					filename = choice[1]
					filepath = os.getcwd()+"/"+filename
					if not os.path.exists(filepath):
						print(f"[FTpy] ERROR: {filename} does not exist.")
					filesize = os.path.getsize(filepath)
					header_sendall(sock,UPLOAD_MESSAGE.encode(FORMAT))
					header_sendall(sock,filename.encode(FORMAT))
					header_sendall(sock,str(filesize).encode(FORMAT))
					left = filesize
					with open(filepath,"rb") as file:
						while left > 0:
							if left < BUFFER_SIZE:
								sock.sendall(file.read(left))
								left = 0
							else:
								sock.sendall(file.read(BUFFER_SIZE))
								left-=BUFFER_SIZE
				elif command == "exit":
					break
				elif command == "help":
					print("help: show help")
					print("ls: list local pwd")
					print("rls: list remote pwd")
					print("download FILENAME: download a file by name from server")
					print("upload FILENAME: upload a file to server by name")
					print("exit: disconnect from server")
				else:
					print("Invalid command.")


				


			header_sendall(sock,DISCONNECT_MESSAGE.encode(FORMAT))
			sock.close()

if __name__ == "__main__":
	main()