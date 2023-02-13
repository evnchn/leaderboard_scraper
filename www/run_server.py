from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import sys

httpd = HTTPServer(('localhost', 6387), BaseHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        certfile=sys.argv[1], 
        keyfile=sys.argv[2], server_side=True)

httpd.serve_forever()