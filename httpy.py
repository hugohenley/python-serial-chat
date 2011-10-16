#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from socket import SHUT_RDWR
import mimetypes
import cgi


class Handler(BaseHTTPRequestHandler):
    def send_404(self):
        self.response('<html><body>Error 404</body></html>', status_code=404)


    def response(self, response, status_code=200,
                      content_type='text/html'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.end_headers()

        self.wfile.write(response)


    def do_GET(self):
        self.method = 'GET'
        self.process_request()


    def process_request(self):
        requested_page = self.path
        if requested_page not in self.urls_and_pages:
            self.send_404()
        else:
            if isinstance(self.urls_and_pages[requested_page], str):
                filename_requested = self.urls_and_pages[requested_page]
                try:
                    file_requested = open(filename_requested)
                except IOError:
                    self.send_404()
                else:
                    response = file_requested.read()
                    file_requested.close()
                    content_type = mimetypes.guess_type(filename_requested)[0]
                    self.response(response, content_type=content_type)
            else:
                function = self.urls_and_pages[requested_page]
                response = function(self)
                status_code = response[0]
                contents = response[1]
                content_type = 'text/html'
                if len(response) == 3:
                    content_type = response[2]
                self.response(contents, status_code=status_code,
                              content_type=content_type)


    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            self.postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            self.postvars = cgi.parse_qs(self.rfile.read(length),
                                         keep_blank_values=1)
        else:
            self.postvars = {}
        self.method = 'POST'
        self.process_request()


class MicroFramework(object):
    def __init__(self, urls_and_pages={}, port=3000):
        self.port = port
        Handler.urls_and_pages = urls_and_pages
        self.httpd = SocketServer.TCPServer(("", self.port), Handler)


    def serve(self):
        self.httpd.timeout = 0.1
        while True:
            try:
                self.httpd.handle_request()
            except KeyboardInterrupt:
                break
        self.httpd.server_close()
