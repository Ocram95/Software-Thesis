import os
import datetime
import psutil
import socket

HOST = 'localhost'
PORT = 5005

RESPONSE = """
HTTP/1.1 {}
Date: {}
Server: Is-Alive Check
Content-Length: {}
Content-Type: text/plain
Access-Control-Allow-Origin: *
{}""" 


def is_running():
    return True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            status = '200 OK'
            text = "I'm alive!"
            
            # Respond
            current = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')
            conn.sendall(RESPONSE.format(status, current, len(text), text).encode())
