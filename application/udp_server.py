import socket

HOST = "10.0.0.2"
PORT = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print("UDP server listening on", HOST, PORT)

while True:
    data, address = server.recvfrom(1024)
    server.sendto(data, address)
