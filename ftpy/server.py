import socket
import os
import threading
from utils import *

LISTENING_HOST = ''
LISTENING_PORT = 9001
FILES = os.getcwd()+"/server-files/"
print(os.path.exists(FILES))

def handle_client(conn,addr):
    print(f"[FTpy] Established connected from {addr}")
    connected = True
    while connected:
        cmd = header_recv(conn).decode(FORMAT).strip()
        if cmd == DISCONNECT_MESSAGE:
            connected = False
        elif cmd == LS_MESSAGE:
            file_list = "\n".join([file for file in os.listdir(FILES)])
            e_file_list = file_list.encode(FORMAT)
            header_sendall(conn,e_file_list)
        elif cmd == DOWNLOAD_MESSAGE:
            filename = header_recv(conn).decode(FORMAT).strip()
            filepath = FILES+filename
            if not os.path.isfile(filepath):
                connected = False
                header_sendall(conn,str(0).encode(FORMAT))
                continue
            filesize = os.path.getsize(filepath)
            print(filesize)
            header_sendall(conn,str(filesize).encode(FORMAT))
            left = filesize
            with open(filepath,"rb") as file:
                while left > 0:
                    if left < BUFFER_SIZE:
                        conn.sendall(file.read(left))
                        left = 0
                    else:
                        conn.sendall(file.read(BUFFER_SIZE))
                        left-=BUFFER_SIZE
        elif cmd == UPLOAD_MESSAGE:
            filename = header_recv(conn).decode(FORMAT).strip()
            filesize = header_recv(conn).decode(FORMAT).strip()
            filesize = int(filesize)
            with open(FILES+filename,"wb") as newfile:      
                left = filesize
                while left > 0:
                    if left < BUFFER_SIZE:
                        newfile.write(conn.recv(left))
                        left = 0
                    else:
                        newfile.write(conn.recv(BUFFER_SIZE))
                        left-=BUFFER_SIZE

    conn.close()
    print(f"[FTpy] {addr} disconnected")

def main():
    with socket.socket() as lsock:
        lsock.setblocking(True)
        lsock.bind((LISTENING_HOST,LISTENING_PORT))

        lsock.listen()
        print("[FTpy] server has been started.")

        while True:
            conn,addr = lsock.accept()
            thread = threading.Thread(target=handle_client,args=(conn,addr))
            thread.start()

if __name__ == "__main__":
    main()