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
import crypto

HEADER_LEN = 8
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
DOWNLOAD_MESSAGE = "UPLOAD"
UPLOAD_MESSAGE = "DOWNLOAD"
LS_MESSAGE = "LIST"
LOGIN_MESSAGE = "LOGIN"
LOGIN_FAILURE_MESSAGE = "FAILURE"
LOGIN_SUCCESS_MESSAGE = "SUCCESS"
HANDSHAKE_PASSWORD = "ftpy"
BUFFER_SIZE = 1024

def header_recv(conn,password=HANDSHAKE_PASSWORD):
    data_len = conn.recv(HEADER_LEN).decode(FORMAT).strip()
    data_len = int(data_len,16)
    data = conn.recv(data_len)
    data = crypto.decrypt_data(password,data,FORMAT)
    return data

def header_sendall(conn,data,password=HANDSHAKE_PASSWORD):
    encrypted_data = crypto.encrypt_data(password,data,FORMAT)
    header = str(len(encrypted_data))
    header = header.zfill(HEADER_LEN).encode(FORMAT)
    packet = header+encrypted_data
    conn.sendall(packet)