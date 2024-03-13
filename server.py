import socket
import secrets
import threading

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_address = '0.0.0.0'
tcp_sever_port = 9002

tcp.bind((tcp_server_address, tcp_sever_port))
tcp.listen(10)
room_names = {}
client_tokens = {}

def handle_tcp_connections():
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
                    connection.send('このルーム名はすでに使われています。'.encode('utf-8'))
                else:
                    # トークンを発行
                    token = secrets.token_hex(8)
                    server_address, ip_address = client_address
                    client_tokens[ip_address] = token
                    room_names[room_name] = password
                    connection.send(token.encode('utf-8'))
                    
            # すでにあるチャットルームに参加
            elif operation_code == '2':
                room_name = connection.recv(4096).decode('utf-8')
                if room_name not in room_names:
                    connection.send('0'.encode('utf-8'))
                if room_names[room_name] is not None:
                    connection.send('1'.encode('utf-8'))
                    password = connection.recv(4096).decode('utf-8')
                    if room_names[room_name] == password:
                        token = secrets.token_hex(8)
                        server_address, ip_address = client_address
                        client_tokens[ip_address] = token
                        #トークンを送る
                        connection.send(token.encode('utf-8'))
                    else:
                        connection.send('1')
            else:
                connection.send('operation code is not found'.encode('utf-8'))
            break
        except Exception as e:
            print(e)
        finally:
            connection.close()
        
        
def handle_udp_connections():     
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = '0.0.0.0'
    server_port = 9001
    sock.bind((server_address, server_port))
    user_arg_set = set()

    try:
        while True:
            token, server_address = sock.recvfrom(4096)
            if token.decode('utf-8') not in client_tokens.values():
                sock.sendto('0'.encode('utf-8'), server_address)
                break
            else:
                sock.sendto('1'.encode('utf-8'), server_address)
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

# TCPとUDPの接続をそれぞれ別のスレッドで処理する
tcp_thread = threading.Thread(target=handle_tcp_connections)
udp_thread = threading.Thread(target=handle_udp_connections)

tcp_thread.start()
udp_thread.start()

# すべてのスレッドが終了するのを待つ
tcp_thread.join()
udp_thread.join()
