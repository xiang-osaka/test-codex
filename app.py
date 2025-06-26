import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_NAME = 'members.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/members':
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('SELECT id, name, contact FROM members')
            rows = c.fetchall()
            members = [ {'id': row[0], 'name': row[1], 'contact': row[2]} for row in rows ]
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps(members).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                name = data.get('name')
                contact = data.get('contact')
                if not name or not contact:
                    raise ValueError('name and contact are required')
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute('INSERT INTO members(name, contact) VALUES (?, ?)', (name, contact))
                conn.commit()
                conn.close()
                self._set_headers(201)
                self.wfile.write(json.dumps({'status': 'registered'}).encode('utf-8'))
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    init_db()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
