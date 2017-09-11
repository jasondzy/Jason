
import socket


udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

udp_socket.bind(('',7766))

data = udp_socket.recvfrom(1024)
print(data)
udp_socket.sendto(b'hello',('192.168.0.107',8080))
