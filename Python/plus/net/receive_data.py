import socket

def main():
    receive = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    receive.bind( ('',7788) )

    receive.sendto(b'test',('192.168.0.107', 8081) )

    while True:
        re_data = receive.recvfrom(1024)
        data,ipinfo = re_data
        receive.sendto(data,ipinfo)
        print(data.decode('gb2312'))

    receive.close()


if __name__ == '__main__':
    main()

