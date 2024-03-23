import socket
import sys
import time

def createHeader(first, second):
    return first.to_bytes(1, 'big') + second.to_bytes(1, 'big')


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_address = '127.0.0.1'
tcp_sever_port = 9002

how = input('please enter operation code?')
user_name = input('enter user name: ')
token = 'aaaa'
join_room_name = ''

try:
    tcp.connect((tcp_server_address, tcp_sever_port))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    header = createHeader(len(user_name), len(how))
    tcp.send(header + user_name.encode('utf-8') + how.encode('utf-8'))
    
    # 新しくルームを作る
    if how == '0':
        response = tcp.recv(4096).decode('utf-8')
        room_name = input('please enter room name:')
        optional = input('do you enter a password?')
        if optional == '0':
            password =input('please enter password')
        if password:
            header = createHeader(len(room_name),len(password))
            tcp.send(header + room_name.encode('utf-8') + password.encode('utf-8'))
        else:
            tcp.send(room_name.encode('utf-8'))
        # 成功すればトークンが返却、もし同じ名前のルームがあればそのメッセージが返ってくる
        token = tcp.recv(4096).decode('utf-8')
        join_room_name = room_name
        tcp.close()
        
    # 既存のルームに参加する
    elif how == '2':
        room_name = input('please enter room name')
        room_name_header = len(room_name).to_bytes(1, 'big')
        tcp.send(room_name_header + room_name.encode('utf-8'))
        response = tcp.recv(4096).decode('utf-8')
        if response == '0':
            print('the room is not found')
            sys.exit(1)
        elif response == '1':
            password = input('please enter password')
            password_header = len(password).to_bytes(1, 'big')
            tcp.send(password_header + password.encode('utf-8'))
            result = tcp.recv(4096).decode('utf-8')
            if result == '1':
                print('your password is wrong. please retry first')
                sys.exit(1)
            else:
                token = result
                join_room_name = room_name
    
finally:
    tcp.close()

time.sleep(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 9001)
# timeout_sec = 10
# sock.settimeout(timeout_sec)
def doUdp():
    print(token)
    try:
        header = createHeader(len(join_room_name), len(token))
        while True:
            message = input('enter message: ')
            message_bits = message.encode('utf-8')
            print(header)
            sock.sendto(header + join_room_name.encode('utf-8') + token.encode('utf-8') + message_bits, server_address)
            data, address = sock.recvfrom(4096)
            if data:
                if data.decode('utf-8') == '0':
                    print('you are not allowed to join this room')
                    sys.exit(1)
                elif data.decode('utf-8') == '1':
                    print(data.decode('utf-8'))
    except socket.timeout:
        print('timeout')
    finally:
        sock.close()

doUdp()
