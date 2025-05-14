from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime


class ForbiddenHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(403, "Forbidden")
        self.send_header('Server', 'nginx/1.18.0')
        self.send_header('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
        self.send_header('Content-Type', 'text/plain')
        self.send_header('X-Request-ID', 'ERR_47_1720463832')
        self.send_header('X-Protected-By', 'WordPress Security Gateway')
        self.end_headers()

        message = """ERROR: Protected Content Access Violation (Code: 403.7)
Request to access protected resource has been blocked by WordPress Enhanced Security Protocol.

Technical Details:
- Error Type: ERR_PROTECTED_CONTENT_ACCESS
- Component: wp-content/plugins/content-protector/security.php
- Protection Level: Maximum
- Access Method: Direct Request Blocked"""

        self.wfile.write(message.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=ForbiddenHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}... (Press CTRL+C to stop)')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
