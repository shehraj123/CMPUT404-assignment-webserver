#  coding: utf-8 
import socketserver
from urllib.parse import urlparse
import mimetypes
from pathlib import Path
import os

# Copyright 2023 Shehraj Singh
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
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        if len(str(self.data.decode('utf-8'))) == 0: 
            return

        method, address = self.parse_request(self.data)


        # Handle GET
        if method == 'GET':
            response = self.generate_response(address)
            self.request.sendall(response)

        # Handle disallowed different methods
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\n", "utf-8"))


    def generate_response(self, address, host="") -> bytearray:

        if address == None:
            return bytearray("HTTP/1.1 404 Not Found\r\n\n", 'utf-8')

        if address.endswith('/'):
            address += 'index.html'

        if address.startswith('/..'):
            return bytearray("HTTP/1.1 404 Not Found\r\n\n", 'utf-8')

        try:
            with open("./www" + address, "r") as file:
                data = file.read()

                header = "HTTP/1.1 200 OK\r\n"
                type, encoding = mimetypes.guess_type("./www" + address)
                
                metadata = "Content-Type: " + type + "\r\n\n"

                response = header + metadata + data + "\r\n\n"

                response = response.encode('utf-8')

                return response

        except FileNotFoundError:
            return bytearray("HTTP/1.1 404 Not Found\r\n\n", 'utf-8')

        except IsADirectoryError:
            # response = bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: http://" + host + address + '/\r\n', 'utf-8')
            response = bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + address + '/\r\n', 'utf-8')
            return response
        except Exception:
            return bytearray("HTTP/1.1 404 Not Found\r\n\n", 'utf-8')

        
        

    def parse_request(self, text: bytearray) -> tuple:

        # Convert back to string
        text = text.decode('utf-8')

        parts = text.split('\n')
        
        # Remove all extra new lines
        # This has to be done according to RFC 2616
        for part in parts:
            if part == '':
                parts.remove(part)
        request = parts[0]

        # Getting the method and the complete address (including hostname) of the request
        method = request.split(' ')[0].strip()

        path = request.split(' ')[1].strip()

        valid_start = os.getcwd() + "/www"
        
        # Checking
        check = Path("www" + path)
        check = check.resolve().as_posix()
        check = str(check)
        
        if not check.startswith(valid_start):
            return method, None

        print(path)
        return method, path
        




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

    
