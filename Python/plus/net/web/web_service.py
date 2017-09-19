
from socket import *
from multiprocessing import Process
import re

def Handle_data(data):

    # split the html name
    html = '.'+(re.match(r'\w+ +(/[^ ]*)', (data.decode('utf-8')).splitlines()[0])).group(1)

    # try to read the local html data
    try:
        file = open(html, 'rb')
        html_data = file.read()
    except:
        print('open file error')
        while True:
            pass
    finally:
        file.close()

        print(html_data)

    # http send data
    send_data = "HTTP/1.1 200 ok\r\n" + "Server: my server" "\r\n" + '\r\n'+ html_data.decode('utf-8')

    return send_data


def  Receive_data(Client):

        # Receive data 
        print('--receive data--')
        data = Client.recv(1024)

        # data is right?
        if data:
            print(data)
            send_data = Handle_data(data)

            Client.send(bytes(send_data, 'utf-8'))
        else:
            print('--data error--')
        
        # close client, only connect one time
        Client.close()


def main():

    Web_service = socket(AF_INET, SOCK_STREAM)
    print('--create a socket--')
    
    Web_service.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    Web_service.bind(('', 7788))
    print('--bind port --')

    Web_service.listen(5)
    print('--listenning--')

    while True:
        Client, ip_info = Web_service.accept()
        print('--accept--')

        # create a Process to receive data and handle it 
        p = Process(target=Receive_data, args=(Client,))
        p.start()

        # when create the Process and transfer the Client. the main process client should be closed
        Client.close()

    Web_service.close()


if __name__ == '__main__':
    main()
