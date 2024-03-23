import socket
import secrets
import threading
import sys

user_arg_set = set()

def handle_client_udp(room_name, token, data, client_address, sock):
    if token not in client_tokens.values():
        sock.sendto('0'.encode('utf-8'), client_address)
    else:
        sock.sendto('1'.encode('utf-8'), client_address)

    user_arg_set.add(client_address)

    for val in user_arg_set:
        if val != client_address:
            sock.sendto(data.decode('utf-8'), val)
        
def handle_udp_connections():   
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = '127.0.0.1'
    server_port = 9001
    sock.bind((server_address, server_port))
    while True:
        try:
            print('UDP server is waiting for connection')
            data, client_address = sock.recvfrom(4096)
            header = data[:2]
            message = data[2:]
            room_name_size = int.from_bytes(header[:1], 'big')
            token_size = int.from_bytes(header[1:2], 'big')

            room_name_data = data[2:room_name_size + 2]
            token_data = data[room_name_size + 2:room_name_size + 2 + token_size]
            room_name = room_name_data.decode('utf-8')
            token = token_data.decode('utf-8')
            message_context = data[room_name_size + token_size + 2:]
            client_thread = threading.Thread(target=handle_client_udp, args=(room_name, token, message_context, client_address, sock))
            client_thread.start()
        except OSError as e:
            print(e)
            
def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise Exception('short read from socket')
        data += more
    return data

room_names = {}
client_tokens = {}

def handle_client(connection, client_address):
    try:
        # ヘッダーの受信
        header = recv_all(connection, 2)
        print(f'9: server header受取 {header}')

        # ユーザー名のサイズと操作コードのサイズを取得
        user_name_size = int.from_bytes(header[:1], 'big')
        operation_code_size = int.from_bytes(header[1:2], 'big')

        # ユーザー名と操作コードの受信
        user_name = recv_all(connection, user_name_size).decode('utf-8')
        operation_code = recv_all(connection, operation_code_size).decode('utf-8')

        print(user_name + ' is login')
        print(f'operation_code is {operation_code}')
        # 新しくルームを作成する
        if operation_code == '0':
            connection.send('please enter room name and password, password is optional'.encode('utf-8'))
            
            information = recv_all(connection, 2)
            room_name_size = int.from_bytes(information[:1], 'big')
            password_size = int.from_bytes(information[1:2], 'big')
            
            room_name = recv_all(connection, room_name_size).decode('utf-8')
            password = recv_all(connection, password_size).decode('utf-8')
            
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
            information = recv_all(connection, 1)
            room_name = recv_all(connection, int.from_bytes(information, 'big')).decode('utf-8')
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
            sys.exit(1)
    except Exception as e:
        print(e)
    finally:
        connection.close()

def handle_tcp_connections(tcp):
    while True:
        connection, client_address = tcp.accept()
        print('server is connected')
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()

def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_address = '0.0.0.0'
    tcp_server_port = 9002
    tcp.bind((tcp_server_address, tcp_server_port))
    tcp.listen(10)
    tcp_thread = threading.Thread(target=handle_tcp_connections, args=(tcp,))
    tcp_thread.start()
    
    udp_thread = threading.Thread(target=handle_udp_connections)
    udp_thread.start()


if __name__ == "__main__":
    main()