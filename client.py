'''
	Copyright (C) 2023 https://github.com/haile-selassie

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import socket
import os
from net import *
 
#PORT = int(input("Enter the port number.\n> "))
#HOST = input("Enter IP address of the server.\n> ")
PORT = 2234
HOST = "192.168.1.106"

def main():
	
	with socket.socket() as sock:
			sock.setblocking(True)
			sock.connect((HOST,PORT))
			print(f"[FTpy] Connected to {HOST}:{PORT}.")
			print("FTpy Copyright (C) 2023 https://github.com/haile-selassie")
			print("This program comes with ABSOLUTELY NO WARRANTY; for details type `warranty'.")
			print("This is free software, and you are welcome to redistribute it")
			print("under certain conditions; see the GNU General Public License for more details.")
			connected = True

			password = input("Enter password:\n> ").strip()
			header_sendall(sock,LOGIN_MESSAGE.encode(FORMAT),password)
			login_response = header_recv(sock).decode(FORMAT)
			if login_response != LOGIN_SUCCESS_MESSAGE:
				connected = False

			home_dir = os.path.expanduser("~")
			os.chdir(home_dir)

			while connected:
				choice = input("FTpy> ").split()
				if len(choice) == 0:
					continue
				command = choice[0]
				if len(command) == 0:
					continue
				if command == "rls":
					header_sendall(sock,LS_MESSAGE.encode(FORMAT),password)
					file_list = header_recv(sock,password).decode().strip()
					print(file_list)
				elif command == "ls":
					file_list = "\n".join([file for file in os.listdir()])
					print(file_list)
				elif command == "download":
					filename = choice[1]
					header_sendall(sock,DOWNLOAD_MESSAGE.encode(FORMAT),password)
					header_sendall(sock,filename.encode(FORMAT),password)
					file_size = header_recv(sock,password).decode(FORMAT).strip()
					file_size = int(file_size)
					if file_size == 0:
						print(f"[FTpy] ERROR: {filename} does not exist.")
						continue
					with open(filename,"wb") as newfile:
						left = file_size
						while left > 0:
							in_data = header_recv(sock,password)
							newfile.write(in_data)
							left-=len(in_data)
					print(f"[FTpy] Downloaded {filename} from {HOST}")
				elif command == "upload":
					filename = choice[1]
					filepath = os.getcwd()+"/"+filename
					if not os.path.exists(filepath):
						print(f"[FTpy] ERROR: {filename} does not exist.")
					filesize = os.path.getsize(filepath)
					header_sendall(sock,UPLOAD_MESSAGE.encode(FORMAT),password)
					header_sendall(sock,filename.encode(FORMAT),password)
					header_sendall(sock,str(filesize).encode(FORMAT),password)
					left = filesize
					with open(filepath,"rb") as file:
						while left > 0:
							if left < BUFFER_SIZE:
								sock.sendall(file.read(left))
								left = 0
							else:
								sock.sendall(file.read(BUFFER_SIZE))
								left-=BUFFER_SIZE
				elif command == "cd":
					new_dir = choice[1]
				elif command == "exit":
					break
				elif command == "warranty":
					print("THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.")
					print("EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES")
					print("PROVIDE THE PROGRAM “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR")
					print("IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND")
					print("FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE")
					print("OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE")
					print("COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.")
				elif command == "help":
					print("help: show help")
					print("ls: list local pwd")
					print("rls: list remote pwd")
					print("download FILENAME: download a file by name from server")
					print("upload FILENAME: upload a file to server by name")
					print("warranty: display warranty details")
					print("exit: disconnect from server")
				else:
					print("Invalid command.")


				


			header_sendall(sock,DISCONNECT_MESSAGE.encode(FORMAT),password)
			sock.close()

if __name__ == "__main__":
	main()