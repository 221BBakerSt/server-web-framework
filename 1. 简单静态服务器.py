from socket import *
from multiprocessing import Pool
import re

def main(serverAddress):
    global serverSocket, clientSocket, clientAddress

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(serverAddress)
    serverSocket.listen(55)
    clientSocket, clientAddress = serverSocket.accept()
    receive()
    read()
    send()
    '''
    p = Pool(4)
    p.apply_async(func = receive, args = (clientSocket,))
    p.apply_async(func = read, args = (HOME,))
    p.apply_async(func = send, args = (clientSocket,))
    p.close()
    p.join()
    '''
    serverSocket.close()


def receive():
    global method, fileName
    
    requestData = clientSocket.recv(1024).decode('utf-8')
    print(requestData)
    #extract method and fileName from requestData
    requestStartLine = requestData.splitlines()[0]
    print('-----------------------')
    print(requestStartLine)
    method = re.match(r'([A-Z]+) /', requestStartLine).group(1)
    fileName = re.match(r'[A-Z]+\s+(/[^\s]*)\s', requestStartLine).group(1)
    if '/' == fileName:
        fileName = fileName + 'index.html'
    print(method)
    print(fileName)

def read():
    global response
    
    if method == 'GET':
        try:
            with open(HOME + fileName, 'rb') as file:
                responseBody = file.read().decode('utf-8')
            responseStartLine = 'HTTP/1.1 200 OK\r\n'
        
        except IOError:
            responseBody = 'The file is not found!'
            responseStartLine = 'HTTP/1.1 404 Not Found\r\n'
    
        responseHeaders = 'Server: My server\r\n'
        response = responseStartLine + responseHeaders + '\r\n' + responseBody
        #print('response is\n', response)


def send():
    clientSocket.send(response.encode('gb2312'))
    clientSocket.close()

if __name__ == '__main__':
    serverAddress = ('192.168.0.19', 1025)
    HOME = '/Users/allen/Desktop'
    main(serverAddress)
