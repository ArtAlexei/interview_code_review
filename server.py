import http.client as client
import http.server as server
import socketserver
import urllib.request as request
from urllib.error import URLError

from bs4 import BeautifulSoup

from functions import add_symbols_to_text, replace_absolute_links, add_content_type_tag
from config import HOST, PORT


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


def modify_response(response: client.HTTPResponse) -> str:
    soup = BeautifulSoup(response.read(), 'lxml')
    soup = add_content_type_tag(soup)
    soup = add_symbols_to_text(soup)
    soup = replace_absolute_links(soup)
    return str(soup)


def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    tcp_server = socketserver.TCPServer(('', PORT), MyProxy)
    print(f'Server started: http://127.0.0.1:{str(PORT)}')
    tcp_server.serve_forever()


if __name__ == "__main__":
    run_server()
