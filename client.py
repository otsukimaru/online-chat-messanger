import socket
import sys

def createHeader(user_name, operation_code):
    return user_name.to_bytes(1, 'big') + operation_code.to_bytes(1, 'big')

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_address = '127.0.0.1'
tcp_sever_port = 9002

how = input('please enter operation code?')
user_name = input('enter user name: ')

try:
    tcp.connect((tcp_server_address, tcp_sever_port))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    header = createHeader(len(user_name), len(how))
    tcp.send(header + user_name.encode('utf-8') + how.encode('utf-8'))
    if how == '0':
        response = tcp.recv(4096).decode('utf-8')
        print(response)
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
        result = tcp.recv(4096).decode('utf-8')
        print(result)
finally:
    tcp.close()
    
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address = ('127.0.0.1', 9001)
# timeout_sec = 10
# sock.settimeout(timeout_sec)

# try:
#     if user_name:
#         print('login:' + user_name)
#         while True:
#             message = input('enter message: ')
            
#             user_name_bits = user_name.encode('utf-8')
#             message_bits = message.encode('utf-8')
#             header = len(user_name_bits).to_bytes(1, 'big') + user_name_bits
#             sock.sendto(header + message_bits, server_address)
            
#             data, server = sock.recvfrom(4096)
#             print(data.decode('utf-8'))
#     else:
#         print("No user name provided.")
# except socket.timeout:
#     print('timeout')
# finally:
#     sock.close()
