import socket
import os

LISTENING_HOST = ''
LISTENING_PORT = 9001

class Connection:
    def __init__(self,sock,addr):
        self.sock = sock
        self.ip = addr[0]
        self.port = addr[1]
        self.pwd = "files"
        sock.setblocking(True)
        print(f"{self.ip} connected on port {self.port}")
    def download(self):
        fn_len = conn.recv()
        filename = conn.recv(1024)
        filename = filename.decode()

        with open(f"files/{filename}","rb") as file:
            while True:
                line = file.read(1024)
                if not line:
                    break
                conn.send(line)

        print(f"{self.ip} has downloaded {filename}")
    def filelist(self):
        filelist = ""
        for file in os.scandir(self.pwd):
            filelist += f"{file.name}\n"
        conn.sendall(filelist.encode())


with socket.socket() as lsock:
    lsock.setblocking(True)
    lsock.bind((LISTENING_HOST,LISTENING_PORT))

    lsock.listen()
    print("FTpy server has been started.")

    while True:
        conn,addr = lsock.accept()
        sock = Connection(conn,addr)
        sock.filelist()
        
        conn.close()