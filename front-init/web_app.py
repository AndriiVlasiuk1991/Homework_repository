import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
from time import sleep
import threading
import json
from datetime import datetime
import os

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/contact':
            self.send_html_file('contact.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        data_dict = {}
        for item in post_data.split('&'):
            key, value = item.split('=')
            data_dict[key] = urllib.parse.unquote_plus(value)

        if 'username' in data_dict and 'message' in data_dict:
            username = data_dict['username']
            message = data_dict['message']
            self.save_message_to_json(username, message)
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Invalid data format')

    def send_html_file(self, filename, sratus=200):
        self.send_response(sratus)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    @staticmethod
    def save_message_to_json(username, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        new_message = {
            "username": username,
            "message": message
        }

        storage_path = "storage"
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        json_path = os.path.join(storage_path, "data.json")

        data = {}
        if os.path.exists(json_path):
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)

        data[timestamp] = new_message

        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def echo_server(host, port):
        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            print(f"Server listening on {host}:{port}")

            while True:
                conn, addr = s.accept()
                print(f"Connected by {addr}")

                with conn:
                    data = conn.recv(1024)
                    if not data:
                        break
                    data_parse = urllib.parse.unquote_plus(data.decode())
                    data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

                    if 'username' in data_dict and 'message' in data_dict:
                        username = data_dict['username']
                        message = data_dict['message']
                        HttpHandler.save_message_to_json(username, message)
                    else:
                        print("Invalid data format")

                    conn.send(b'Message received and saved')

    @staticmethod
    def simple_client(host, port):
        with socket.socket() as s:
            while True:
                try:
                    s.connect((host, port))
                    s.sendall(b'Hello, world')
                    data = s.recv(1024)
                    print(f'From server: {data}')
                    break
                except ConnectionRefusedError:
                    sleep(0.5)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
    HOST = '127.0.0.1'
    PORT = 5000

    server = threading.Thread(target=HttpHandler.echo_server, args=(HOST, PORT))
    client = threading.Thread(target=HttpHandler.simple_client, args=(HOST, PORT))

    server.start()
    client.start()
    server.join()
    client.join()
    print('Done!')
