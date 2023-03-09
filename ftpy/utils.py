HEADER_LEN = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
DOWNLOAD_MESSAGE = "UPLOAD"
UPLOAD_MESSAGE = "DOWNLOAD"
LS_MESSAGE = "LIST"
BUFFER_SIZE = 1024

def header_recv(conn):
    data_len = conn.recv(HEADER_LEN).decode(FORMAT).strip()
    data_len = int(data_len,16)
    data = conn.recv(data_len)
    return data

def header_sendall(conn,e_data):
    header = str(len(e_data))
    header = header.zfill(HEADER_LEN).encode(FORMAT)
    packet = header+e_data
    conn.sendall(packet)