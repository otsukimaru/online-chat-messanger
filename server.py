import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001

sock.bind((server_address, server_port))
user_arg_set = set()

try:
    while True:
        header, client_address = sock.recvfrom(4096)
        user_arg_set.add(client_address)

        if header:
            user_name_length = int.from_bytes(header[:1], 'big')
            user_name = header[1:user_name_length+1]
            message = header[user_name_length+1:]

            if user_name_length == 0:
                sock.sendto('not allow empty of user name')
                raise Exception('user name is empty')
            
            print('login:' + user_name.decode('utf-8'))
            for val in user_arg_set:
                if val != client_address:
                    sent = sock.sendto(message, val)
finally:
    sock.close()
