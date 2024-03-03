import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001

sock.bind((server_address, server_port))

try:
    while True:
        data, client_address = sock.recvfrom(4096)

        if data:
            sent = sock.sendto(data, client_address)
finally:
    sock.close()