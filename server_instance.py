# importing necessary dependencies
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from remote_memory import read_json_from_s3, upload_json_to_s3, SHARED_OBJECT_NAME
from urllib.parse import urlparse, parse_qs
from utils import get_server_uri


# This function returns a HTTP server instance
# This accepts 2 user defined parameters which are Address and Port 
# which are the necessary variables to create sockets and create a server.

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        shared_object = read_json_from_s3()
        self.send_response(200, "3")
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Success"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        length = int(self.headers['content-length'])
        url_string = get_server_uri(self.server) + "?" + str(self.rfile.read(length), "UTF-8")
        parsed_url = urlparse(url_string)
        data = parse_qs(parsed_url.query)
        duration = 0
        if "PEER_SERVER_CONN_URI" in data and  data["PEER_SERVER_CONN_URI"] is not None:
            PEER_SERVER_CONN_URI = data["PEER_SERVER_CONN_URI"][0]
            res = requests.post(PEER_SERVER_CONN_URI, { "id": data["id"][0], "timestamp": data["timestamp"][0] })
            duration = res.elapsed.total_seconds()
        
        self.send_response(200, str(duration))
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = str(duration)
        self.wfile.write(bytes(message, "utf8"))
    
    def do_PUT(self):
        length = int(self.headers['content-length'])
        url_string = get_server_uri(self.server) + "?" + str(self.rfile.read(length), "UTF-8")
        parsed_url = urlparse(url_string)
        data = parse_qs(parsed_url.query)
        filename = upload_json_to_s3(json.dumps(data, indent=2).encode('utf-8'))

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Success!"
        self.wfile.write(bytes(message, "utf8"))

def return_server_instance(ADDRESS, PORT):
    server_address = (ADDRESS, PORT)
    # HTTPServer function accepts 2 parameters: server_address 
    # consisting of a tuple (Address, Port) and a handler class.
    # It returns a server instance.
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.allow_reuse_address = True
    print("Server running at", get_server_uri(httpd))
    httpd.serve_forever()
    return httpd

