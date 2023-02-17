import socket
 
PORT = int(input("Enter the port number.\n> "))
HOST = input("Enter IP address of the server.\n> ")
 
with socket.socket() as sock:
	sock.setblocking(True)
	sock.connect((HOST,PORT))
	print(f"Connected to {HOST}:{PORT}.")
	print("Retrieving file list...")
 
	filelist = b''
	while True:
		data = sock.recv(1024)
		if len(data) < 1024:
			filelist+=data
			break
		filelist+=data
 
	print("Choose a file to download: ")
	print(filelist.decode())
	filename = input("> ")
	sock.send(filename.encode())
 
	print(f"Downloading {filename}...")
	with open(filename,"wb") as file:
		while True:
			data = sock.recv(1024)
			if len(data) < 1024:
				file.write(data)
				break
			file.write(data)
	print(f"{filename} has been saved successfully.")
	sock.close()
