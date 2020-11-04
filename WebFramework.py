from MyServer import HTTP_Server

class Framework(object):
    '''the universal framework'''
    def __init__(self, urls):
        # set routing info
        self.urls = urls

    def __call__(self, env, start_response):
        
        path = env.get('PATH_INFO', '/')
        if path.endswith('.html'):
            file_name = path
            headers = [('Server', 'My Server'), ('Content-Type', 'text/html;charset=UTF-8')]
            try:
                with open(HOME + file_name, 'rb') as file:
                    response_body = file.read().decode('utf-8')
                # response_start_line = 'HTTP/1.1 200 OK\r\n'
                status = '200 OK'
                start_response(status, headers)
                return response_body

            except IOError:
                status = '404 Not Found'
                start_response(status, headers)
                response_body = 'page not found'
                return response_body

        for url, func in self.urls.items():
            if path == url:
                return func(env, start_response)

        status = '404 Not Found'
        headers = [('Server', 'My Server'), ('Content-Type', 'text/html;charset=UTF-8')]
        start_response(status, headers)
        response_body = 'page not found'
        return response_body
########################################################################################
'''add a func for an url'''

def ctime(env, start_response):
    import time
    status = '200 OK'
    headers = [('Server', 'My Server'), ('Content-Type', 'text/html;charset=UTF-8')]
    start_response(status, headers)
    return time.ctime()

def sayhello(env, start_response):
    status = '200 OK'
    headers = [('Server', 'My Server'), ('Content-Type', 'text/html;charset=UTF-8')]
    start_response(status, headers)
    return 'say hello!'

server_address = ('192.168.0.19', 1025)
HOME = '/Users/allen/Desktop'
urls = {'/ctime':ctime, '/sayhello':sayhello}
app = Framework(urls)

if __name__ == '__main__':

    # server_address = ('192.168.0.19', 1025)
    # HOME = '/Users/allen/Desktop'
    # urls = {'/ctime':ctime, '/sayhello':sayhello}
    # app = Framework(urls)
    server = HTTP_Server(server_address, app)
    server.receive()
    server.send()
