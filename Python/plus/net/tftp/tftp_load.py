
import struct 

import socket

def download_file(name,data):
	f = open(name,'ab') #注意这里一定要以字节追加的形式打开，因为tftp发送过来的就是字节型的数据，所以将字节型的数据直接写入到文件中即可。其他形式不可以
	f.write(data)

	f.close()



def main():
    name = input('---please input which file you want to load----')
    struct_info = '!H' + str(len(name)) + 'sb5sb'
    print(struct_info)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #创建UDP对象

    send_data = struct.pack(struct_info, 1, name.encode('utf-8'), 0, b"octet", 0)#此处的作用是使用struct模块对要发送的数据按照tftp的信息格式进行封装，具体的信息见课件中tftp的信息格式

    udp_socket.sendto(send_data, ('192.168.0.107', 69))#这里对上面封装好了的数据发往69号端口，此端口是tftp默认的首次通信端口，接下来的数据通信端口就不在是69号端口了，而是采用的动态端口的方式，所以再往69端口发数据就不会有任何响应

    while True:
        receive_data = udp_socket.recvfrom(1024)#再发送完数据后，tftp就会返回进行封装了的512字节的数据，这里接收的时候并不需要绑定端口，因为tftp会根据所接收到的数据解析出所用的端口

        data,ip_info = receive_data #对接收到的信息进行解析，因为网络通信中接收到的信息是一个tuple类型的数据，tuple的首个元素是封装的数据，第二个元素是ip地址信息

        cmd_info = data[:4]#获取数据中前四个字节的信息，根据tftp协议，前四个字节有特殊作用，4个字节后的512个字节才是真正的数据

        cmd_info = struct.unpack('!HH',cmd_info)#这里是将接收到的数据进行解析，这里解析到的cmd_info是一个tuple,(3,1)
        

        print(cmd_info)
        print(data[4:])

        if cmd_info[0] == 3:
            download_file(name,data[4:])
            if len(data[4:])<512:
                print('---receive data end-------')
                break
            
            print('------------receive next  512 bytes data---------')
            ACK = struct.pack('!HH',4,cmd_info[1])
            udp_socket.sendto(ACK,ip_info)
        else:
            break



    udp_socket.close()



if __name__ == '__main__':
	main()
