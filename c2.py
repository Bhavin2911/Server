import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '192.168.0.13'  # client machine ip
port = 4005

server = ('192.168.0.112', 4000)

print('Waiting for connection')
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

message = input("-> ")
while message != 'q':
    s.sendto(message.encode('utf-8'), (host, port))
    data, addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    print("Received from server: " + data)
    message = input("-> ")

s.close()
