import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 9001)
message = input('enter message')


try:
    sock.sendto(message.encode('utf-8'), server_address)
    data, server = sock.recvfrom(4096)
    print(data.decode('utf-8'))
finally:
    sock.close()