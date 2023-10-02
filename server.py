#  coding: utf-8 
import socketserver
import os
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    headers = {
        'Server' : 'CrudeServer',
        'Content-Type' : 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }
    
    def handle(self):
        #print(os.path.realpath('index.html'))
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        self.url = self.data.splitlines()[0].split()[1]
        #print("Got a url of: %s\n" % self.url)
        #print(self.data)

        #print(request)


        path = self.url
        #print(path)
        if path == b"/":
            filename = "www/index.html"
            #req = request.urlopen('http://127.0.0.1:8080', None, 3)
            #print("Got response of: %s\n" % req)
        elif path == b"/base.css":
            filename = "www/base.css"
        elif path == b"/index.html":
            filename = "www/index.html"
        elif path == b"/base.css":
            filename = "www/base.css"
        elif path == b"/hardcode/index.html":
            filename = "www/index.html"
        elif path == b"/hardcode/base.css":
            filename = "www/base.css"
        elif path == b"/deep/index.html":
            filename = "www/deep/index.html"
        elif path == b"/deep/deep.css":
            filename = "www/deep/deep.css"
        elif path == b"/deep/":
            filename = "www/deep/index.html"
        elif path == b"/deep/deep.css":
            filename = "www/deep/deep.css"
        else:
            filename = ''

        if os.path.exists(filename) and not os.path.isdir(filename):
            response_line = self.response_line(200)
            #print('this happened 2')
            # find out a file's MIME type
            # if nothing is found, just send `text/html`
            content_type = mimetypes.guess_type(filename)[0] or 'text/html'

            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)

            with open(filename, 'rb') as f:
                response_body = f.read()

        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = b'<h1>404 Not Found</h1>'
            #print('this happened4')

        blank_line = b'\r\n'

        response = b''.join([response_line, response_headers, blank_line, response_body])
        #print(response)
        response = self.request.sendall(response)
        #return response

        return response
    
    def response_line(self, status_code):
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)

        return line.encode()
    
    def response_headers(self, extra_headers=None):

        headers_copy = self.headers.copy()

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode()

    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    #print(server)

    # print(os.path.realpath('index.html'))

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

