from socket import *
from multiprocessing import Pool
import re


class HTTP_Server(object):

    def __init__(self, server_address):

        self.server_address = server_address
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(55)
        self.client_socket, self.client_address = self.server_socket.accept()   

    def __del__(self):
        self.server_socket.close()

    def receive(self):
        
        request_data = self.client_socket.recv(1024).decode('utf-8')
        print(request_data)
        # extract method and file_name from request_data
        request_start_line = request_data.splitlines()[0]
        print('-----------------------')
        print(request_start_line)
        self.method = re.match(r'([A-Z]+) /', request_start_line).group(1)
        self.file_name = re.match(r'[A-Z]+\s+(/[^\s]*)\s', request_start_line).group(1)
        print('method:', self.method)
        print('file name:', self.file_name)
        if self.file_name.endswith('.py'):
            HTTP_Server.load(self)
        else:
            if self.file_name == '/':
                self.file_name += 'index.html'
            HTTP_Server.read(self)


    def start_response(self, status, headers):
        '''provide response_headers'''

        self.response_headers = 'HTTP/1.1 ' + status + '\r\n'
        for header in headers:
            self.response_headers += f'{header[0]}: {header[1]}\r\n'


    def load(self):
        '''dynamic web server'''

        # equal to import XXX as a mod
        mod = __import__(self.file_name[1:-3]) #the slice removes '/' and '.py'
        # create response info
        env = {}
        # env includes the requested data by the browser
        response_body = mod.application(env, self.start_response)
        # func application returns response body
        self.response = self.response_headers + '\r\n' + response_body
        # print('response is\n', response)


    def read(self):
        '''static web server'''
        
        if self.method == 'GET':
            try:
                with open(HOME + self.file_name, 'rb') as file:
                    response_body = file.read().decode('utf-8')
                response_start_line = 'HTTP/1.1 200 OK\r\n'
            
            except IOError:
                response_body = 'The file is not found!'
                response_start_line = 'HTTP/1.1 404 Not Found\r\n'
            
            # create response info
            self.response_headers = 'Server: My server\r\nContent-Type: text/html;charset=UTF-8\r\n'
            self.response = response_start_line + self.response_headers + '\r\n' + response_body
            # print('response is\n', response)

        else:
            print('can\'t handle this method...')


    def send(self):
        self.client_socket.send(self.response.encode('utf-8'))
        self.client_socket.close()


if __name__ == '__main__':
    server_address = ('192.168.0.19', 1025)
    HOME = '/Users/allen/Desktop'
    while 1:
        server = HTTP_Server(server_address)
        server.receive()
        server.send()
        server.__del__()
    '''
    p = Pool(4)
    p.apply_async(func = receive, args = (client_socket,))
    p.apply_async(func = read, args = (HOME,))
    p.apply_async(func = send, args = (client_socket,))
    p.close()
    p.join()
    '''
