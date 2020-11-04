from socket import *
from multiprocessing import Pool
import re

def main(server_address):
    global server_socket, client_socket, client_address

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(55)
    client_socket, client_address = server_socket.accept()
    receive()
    send()
    '''
    p = Pool(4)
    p.apply_async(func = receive, args = (client_socket,))
    p.apply_async(func = read, args = (HOME,))
    p.apply_async(func = send, args = (client_socket,))
    p.close()
    p.join()
    '''
    server_socket.close()


def receive():
    global method, file_name
    
    request_data = client_socket.recv(1024).decode('utf-8')
    print(request_data)
    #extract method and file_name from request_data
    request_start_line = request_data.splitlines()[0]
    print('-----------------------')
    print(request_start_line)
    method = re.match(r'([A-Z]+) /', request_start_line).group(1)
    file_name = re.match(r'[A-Z]+\s+(/[^\s]*)\s', request_start_line).group(1)
    print('method:', method)
    print('file name:', file_name)
    if file_name.endswith('.py'):
        load()
    else:
        if file_name == '/':
            file_name = file_name + 'index.html'
        read()


def start_response(status, headers):
    '''provide response_headers'''
    global response_headers

    response_headers = 'HTTP/1.1 ' + status + '\r\n'
    for header in headers:
        response_headers += f'{header[0]}: {header[1]}\r\n'


def load():
    '''dynamic web server'''
    global response

    #equal to import XXX as mod
    mod = __import__(file_name[1:-3]) #the slice removes '/' and '.py'
    #create response info
    env = {}
    #env includes the requested data by the browser
    response_body = mod.application(env, start_response)
    #func application returns response body
    response = response_headers + '\r\n' + response_body
    #print('response is\n', response)


def read():
    '''static web server'''
    global response
    
    if method == 'GET':
        try:
            with open(HOME + file_name, 'rb') as file:
                response_body = file.read().decode('utf-8')
            response_start_line = 'HTTP/1.1 200 OK\r\n'
        
        except IOError:
            response_body = 'The file is not found!'
            response_start_line = 'HTTP/1.1 404 Not Found\r\n'
        
        #create response info
        response_headers = 'Server: My server\r\nContent-Tyoe: text/html;charset=UTF-8\r\n'
        response = response_start_line + response_headers + '\r\n' + response_body
        #print('response is\n', response)

    else:
        print('can\'t handle this method...')


def send():
    client_socket.send(response.encode('gb2312'))
    client_socket.close()

if __name__ == '__main__':
    server_address = ('192.168.0.19', 1025)
    HOME = '/Users/allen/Desktop'
    main(server_address)
