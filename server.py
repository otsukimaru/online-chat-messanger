import socket
import secrets

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_address = '0.0.0.0'
tcp_sever_port = 9002

tcp.bind((tcp_server_address, tcp_sever_port))
tcp.listen(10)
room_names = {}
client_tokens = {}

while True:
    connection, client_address = tcp.accept()
    try:
        request = connection.recv(2)
        user_name_size = int.from_bytes(request[:1], 'big')
        operation_code_size = int.from_bytes(request[1:2], 'big')
        user_name = connection.recv(user_name_size).decode('utf-8')
        operation_code = connection.recv(operation_code_size).decode('utf-8')
        
        # 新しくルームを作成する
        if operation_code == '0':
            connection.send('please enter room name and password, password is optional'.encode('utf-8'))
            information = connection.recv(2)
            room_name_size = int.from_bytes(information[:1], 'big')
            password_size = int.from_bytes(information[1:2], 'big')
            room_name = connection.recv(room_name_size).decode('utf-8')
            password = connection.recv(password_size).decode('utf-8')
            if room_name in room_names:
                connection.send('このルーム名はすでに使われています。')
            else:
                # トークンを発行
                token = secrets.token_hex(8)
                server_address, ip_address = client_address
                client_tokens[ip_address] = token
                room_names[room_name] = password
                
        # すでにあるチャットルームに参加
        elif operation_code == 2:
            connection.send('please enter room name')
            room_name = connection.recv(1).decode('utf-8')
            
            if room_name not in room_names:
                connection.send('0')
            if room_names[room_name] is not None:
                connection.send('1')
                password = connection.recv(1).decode('utf-8')
                if room_names[room_name] == password:
                    token = secrets.token_hex(8)
                    server_address, ip_address = client_address
                    client_tokens[ip_address] = token
                    #トークンを送る
                    connection.send(token.encode('utf-8'))
                else:
                    connection.send('1')
        break
    except Exception as e:
        print(e)
    finally:
        connection.close()
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server_address = '0.0.0.0'
# server_port = 9001

# sock.bind((server_address, server_port))
# user_arg_set = set()

# try:
#     while True:
#         header, client_address = sock.recvfrom(4096)
#         user_arg_set.add(client_address)

#         if header:
#             user_name_length = int.from_bytes(header[:1], 'big')
#             user_name = header[1:user_name_length+1]
#             message = header[user_name_length+1:]

#             if user_name_length == 0:
#                 sock.sendto('not allow empty of user name')
#                 raise Exception('user name is empty')
            
#             print('login:' + user_name.decode('utf-8'))
#             for val in user_arg_set:
#                 if val != client_address:
#                     sent = sock.sendto(message, val)
# finally:
#     sock.close()
