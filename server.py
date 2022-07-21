import http.server as server
import socketserver
import urllib.request as request
from urllib.error import URLError

from config import HOST, PORT
from functions import modify_response


class MyProxy(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            response = request.urlopen(HOST + self.path)
        except URLError:
            self.send_response(500, f'{HOST} not available')
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        headers = dict(response.headers)
        if 'text/html' in headers['Content-Type']:
            html = modify_response(response)
            self.wfile.write(html.encode('utf-8'))
        else:
            self.copyfile(response, self.wfile)


def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    tcp_server = socketserver.TCPServer(('', PORT), MyProxy)
    print(f'Server started at http://127.0.0.1:{str(PORT)}')
    tcp_server.serve_forever()


if __name__ == "__main__":
    run_server()
