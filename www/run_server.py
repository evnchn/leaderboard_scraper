from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import sys

httpd = HTTPServer(('localhost', 6387), BaseHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile=sys.argv[0], 
        certfile=sys.argv[1], server_side=True)

httpd.serve_forever()