import socket
import os
import threading
from futils import *

LISTENING_HOST = ''
LISTENING_PORT = 9001

def handle_client(conn,addr):
    print(f"[FTpy] Established connected from {addr}")
    connected = True
    while connected:
        msg = header_recv(conn).decode(FORMAT).strip()
        if msg == DISCONNECT_MESSAGE:
            connected = False

    conn.close()
    print(f"[FTpy] {addr} disconnected")

def main():
    with socket.socket() as lsock:
        lsock.setblocking(True)
        lsock.bind((LISTENING_HOST,LISTENING_PORT))

        lsock.listen()
        print("FTpy server has been started.")

        while True:
            conn,addr = lsock.accept()
            thread = threading.Thread(target=handle_client,args=(conn,addr))
            thread.start()