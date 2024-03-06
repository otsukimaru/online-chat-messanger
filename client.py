import socket

how = input('what are yo go ing to do?')
user_name = input('enter user name: ')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 9001)
timeout_sec = 10
sock.settimeout(timeout_sec)

try:
    if user_name:
        print('login:' + user_name)
        while True:
            message = input('enter message: ')
            
            user_name_bits = user_name.encode('utf-8')
            message_bits = message.encode('utf-8')
            header = len(user_name_bits).to_bytes(1, 'big') + user_name_bits
            sock.sendto(header + message_bits, server_address)
            
            data, server = sock.recvfrom(4096)
            print(data.decode('utf-8'))
    else:
        print("No user name provided.")
except socket.timeout:
    print('timeout')
finally:
    sock.close()
