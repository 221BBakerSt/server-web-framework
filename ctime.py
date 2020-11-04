import time

response_body = time.ctime()

def application(env, start_response):
    status = '200 OK'
    headers = [('Server', 'My Server'), ('Content-Type', 'text/html;charset=UTF-8')]
    start_response(status, headers)
    return response_body
