
from socket import *
from multiprocessing import Process
import re


class Http_service(object):
    ''' For Http_service '''
    def __init__(self):
        self.send_data = ''

        self.Web_service = socket(AF_INET, SOCK_STREAM)
        print('--create a socket--')
        
        self.Web_service.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.Web_service.bind(('', 7788))
        print('--bind port --')

    def Http_start(self):
        self.Web_service.listen(5)
        print('--listenning--')

        while True:
            Client, ip_info = self.Web_service.accept()
            print('--accept--')

            # create a Process to receive data and handle it 
            p = Process(target=self.Receive_data, args=(Client,))
            p.start()

        # when create the Process and transfer the Client. the main process client should be closed
            Client.close()

        self.Web_service.close()

    def Receive_data(self, Client):
            # Receive data 
        print('--receive data--')
        data = Client.recv(1024)

        # data is right?
        if data:
            print(data)

            self.Handle_data(data)

            Client.send(bytes(self.send_data, 'utf-8'))
        else:
            print('--data error--')
        
        # close client, only connect one time
        Client.close()    

    def Handle_data(self, data):
        # split the html name
        html = '.'+(re.match(r'\w+ +(/[^ ]*)', (data.decode('utf-8')).splitlines()[0])).group(1)

        # try to read the local html data
        try:
           file = open(html, 'rb')
           html_data = file.read()
        except:
            print('open file error')
            while True:
              print('-----------')
        finally:
            file.close()

        print(html_data)

        # http send data
        self.send_data = "HTTP/1.1 200 ok\r\n" + "Server: my server" "\r\n" + '\r\n'+ html_data.decode('utf-8')




def main():
    http = Http_service()

    http.Http_start()


if __name__ == '__main__':
    main()
