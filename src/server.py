import json
import socket
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def handle_request(self, method):
        headers = dict(self.headers)
        if 'Origin' in headers:
            origin = headers['Origin']
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Access-Control-Allow-Credentials', 'true')
        path = self.path
        result = urlparse(path)
        path = result.path
        switch = {
            '/api/login': self.login,
            '/api/logout': self.logout
        }
        switch.get(path, self.default)(method)

    def login(self, method):
        if method == 'POST':
            self.send_response(HTTPStatus.OK)
            data = {
                'errcode': 0,
                'errmsg': 'ok'
            }
            data = json.dumps(data)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Content-Type', 'application/json;charset=utf-8')
            session = ''
            self.send_header('Set-Cookie', 'session=%s;Path=/;HttpOnly;SameSite=Lax' % session)
            self.end_headers()
            self.wfile.write(data.encode())
        else:
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)

    def logout(self, method):
        if method == 'GET':
            self.send_response(HTTPStatus.OK)
            data = {
                'errcode': 0,
                'errmsg': 'ok'
            }
            data = json.dumps(data)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Content-Type', 'application/json;charset=utf-8')
            self.send_header('Set-Cookie', 'session=;Path=/;Expires=0;HttpOnly;SameSite=Lax')
            self.end_headers()
            self.wfile.write(data.encode())
        else:
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)

    def default(self, method):
        self.send_error(HTTPStatus.NOT_FOUND)


def main():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    host = (ip, 8087)
    print('Starting server, listen at: %s:%s' % host)
    server = HTTPServer(host, HTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
