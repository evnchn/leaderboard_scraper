import http.server
import ssl
import sys


HOST = '192.168.50.208'
PORT = 6387
Handler = http.server.SimpleHTTPRequestHandler
with http.server.HTTPServer((HOST, PORT), Handler) as httpd:
    print("Web Server listening at => " + HOST + ":" + str(PORT))
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslcontext.load_cert_chain(keyfile=sys.argv[2], certfile=sys.argv[1])
    httpd.socket = sslcontext.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()