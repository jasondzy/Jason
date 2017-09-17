"""
# note: 这里是通过gevent模块还实现单线程多任务的功能,其中的socket函数来自gevent模块中
#
#

"""
from gevent import socket, monkey
import gevent

monkey.patch_all()#使用gevent中的monkey来对接一下的函数进行封装成非阻塞的功能，此处必须

def handle_data(client):
    while True:
        data = client.recv(1024)
        if data:
            print(data)
        else:
            client.close()
            break


def main():
    service = socket.socket()
    print('create a socket')

#    service.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    service.bind(('', 7788))
    print('bind a port')

    service.listen(5)
    print('listenning.....')

    while True:
        client,ip = service.accept()
        print('accept..')

        gevent.spawn(handle_data,client)#添加需要进行调度的函数，只要遇到阻塞类型的函数就会进行切换从而实现多任务

    service.close()#never to run here for service

if __name__ == '__main__':
    main()