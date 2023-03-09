import socket
import os
import threading
from utils import *

LISTENING_HOST = ''
LISTENING_PORT = 9001
FILES = "ftpy/files"

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