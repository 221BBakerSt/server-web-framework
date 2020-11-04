from socket import *
from multiprocessing import Pool
import re
import sys


class HTTP_Server(object):

    def __init__(self, server_address, app):
        
        self.server_address = server_address
        self.app = app
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # set the address to be reused(no "Address already in use" error)
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
        HTTP_Server.load(self)


    def start_response(self, status, headers):
        '''provide response_headers'''

        self.response_headers = 'HTTP/1.1 ' + status + '\r\n'
        for header in headers:
            self.response_headers += f'{header[0]}: {header[1]}\r\n'


    def load(self):
        '''will be processed by the router'''

        # create response info
        env = {'PATH_INFO':self.file_name, 'METHOD':self.method}
        # env includes the requested data by the browser
        response_body = self.app(env, self.start_response)
        # func application returns response body
        self.response = self.response_headers + '\r\n' + response_body
        # print('response is\n', response)

    def send(self):
        self.client_socket.send(self.response.encode('utf-8'))
        self.client_socket.close()


if __name__ == '__main__':

    HOME = '/Users/allen/Desktop'
    server_address = ('192.168.0.19', 1025)
    # python3 MyServer.py WebFramework:app
    if len(sys.argv) < 2:
        sys.exit('Hint: python3 MyServer.py framework_module_name:object_name')
    module_name, obj_name = sys.argv[1].split(':')
    mod = __import__(module_name)
    app = getattr(mod, obj_name)
    while 1:
        server = HTTP_Server(server_address, app)
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
