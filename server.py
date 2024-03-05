import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001

sock.bind((server_address, server_port))

try:
    while True:
        header, client_address = sock.recvfrom(4096)

        if header:
            user_name_length = int.from_bytes(header[:1], 'big')
            user_name = header[1:user_name_length+1]
            message = header[user_name_length+1:]

            if user_name_length == 0:
                sock.sendto('not allow empty of user name')
                raise Exception('user name is empty')
            print('login:' + user_name.decode('utf-8'))
            sent = sock.sendto(message, client_address)
finally:
    sock.close()
