import os
import datetime
import psutil
import socket

HOST = '0.0.0.0'
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
    if not os.path.exists('pid.lock'):
        return False
    
    # Read PID
    # Our Testing tool creates a temporary file, containing the PID which will 
    # be removed when the process is interrupted or closed.
    f = open('pid.lock', 'r')
    pid = f.read()
    f.close()
    
    # Parse PID
    pid = pid.strip()
    if len(pid) == 0 or not pid.isnumeric():
        return False
    
    # Check if process is running (supported by Windows as well)
    return psutil.pid_exists(int(pid))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            # Check if test-service is running
            if is_running():
                status = '200 OK'
                text = "I'm alive!"
            else:
                status = '503 Service Unavailable'
                text = "I'm dead!"
            
            # Respond
            current = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')
            conn.sendall(RESPONSE.format(status, current, len(text), text).encode())
