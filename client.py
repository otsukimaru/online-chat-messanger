import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 9050)
user_name = input('enter user name')
message = input('enter message')

def createHeader(user_name, json_length, data_length):
    return user_name.to_bytes(1, 'big') + json_length.to_bytes(3, 'big') + data_length.to_bytes(4, 'big')

try:
    user_name_bits = user_name.encode('utf-8')
    message_bits = message.encode('utf-8')
    header = createHeader(len(user_name_bits), 0,message_bits)
    sock.sendto(header, server_address)
    data, server = sock.recvfrom(4096)
    print(data.decode('utf-8'))
finally:
    sock.close()