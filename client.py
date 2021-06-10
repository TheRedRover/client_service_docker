import socket
import sys
import time
import os


def log(data: str):
    with open("data.txt", mode="a") as f:
        f.write(f"{data}\n")


server_host = None
server_port = None
client_host = "0.0.0.0"
client_port = None
L = 0
while True:
    try:
        server_host = os.environ["SERVER_SERVICE_HOST"]
        server_port = os.environ["CLIENT_SERVICE_PORT"]
        client_port = os.environ["CLIENT_SERVICE_PORT"]
        break
    except KeyError:
        log(f"Try env #{L}")
        L += 1
        time.sleep(5)

log(f"Got SERVER_HOST is {server_host}")
log(f"Got SERVER_PORT is {server_port}")
log(f"Got CLIENT_HOST is {client_host}")
log(f"Got CLIENT_PORT is {client_port}")

remote_address = (server_host, int(server_port))
self_address   = (client_host, int(client_port))


N = 0

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    while True:
        try:
            sock.connect(remote_address)
            break
        except Exception as e:
            pass
    sock.sendall(f"Ping #{N}".encode())
    sock.shutdown(socket.SHUT_WR)
    sock.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(self_address)    sock.listen(10)
    conn, addr = sock.accept()  # blocking
    data = conn.recv(512)
    log(data.decode())
    conn.close()
    sock.close()
    N += 1
    time.sleep(5)

    
