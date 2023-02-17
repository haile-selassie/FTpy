import socket
import os

LISTENING_HOST = ''
LISTENING_PORT = 9001

with socket.socket() as sock:
    sock.setblocking(True)
    sock.bind((LISTENING_HOST,LISTENING_PORT))

    sock.listen()
    print("FTpy server has been started.")

    while True:
        conn,addr = sock.accept()
        client_ip = addr[0]
        client_port = addr[1]
        print(f"{client_ip} connected on port {client_port}")
        
        filelist = ""
        for file in os.scandir("files"):
            filelist += f"{file.name}\n"
        conn.sendall(filelist.encode())

        filename = conn.recv(1024)
        filename = filename.decode()

        with open(f"files/{filename}","rb") as file:
            while True:
                line = file.read(1024)
                if not line:
                    break
                conn.send(line)

        print(f"{client_ip} has downloaded {filename}")        
        conn.close()