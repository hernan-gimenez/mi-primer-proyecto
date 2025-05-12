from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import urllib.parse

LINKS_FILE = 'links.json'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == '/':
            self._serve_file('index.html')
        elif self.path == '/links':
            self._get_links()
        else:
            self._serve_file(self.path[1:])

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            self._save_link(data['link'])
            self._set_headers('application/json')
            self.wfile.write(json.dumps({"status": "success"}).encode())

    def do_DELETE(self):
        if self.path.startswith('/delete/'):
            try:
                index = int(self.path.split('/')[-1])
                self._delete_link(index)
                self._set_headers('application/json')
                self.wfile.write(json.dumps({"status": "deleted"}).encode())
            except (ValueError, IndexError):
                self.send_error(400, "Invalid index")

    def _serve_file(self, filename):
        try:
            if not os.path.isfile(filename):
                self.send_error(404, "File not found")
                return

            with open(filename, 'rb') as f:
                self._set_headers()
                self.wfile.write(f.read())
        except Exception as e:
            self.send_error(500, str(e))

    def _load_links(self):
        if not os.path.exists(LINKS_FILE):
            return []
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_links(self, links):
        with open(LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(links, f)

    def _get_links(self):
        links = self._load_links()
        self._set_headers('application/json')
        self.wfile.write(json.dumps(links).encode())

    def _save_link(self, link):
        links = self._load_links()
        links.append(link)
        self._save_links(links)

    def _delete_link(self, index):
        links = self._load_links()
        if 0 <= index < len(links):
            del links[index]
            self._save_links(links)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
