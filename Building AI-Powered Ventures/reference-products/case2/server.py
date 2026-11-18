#!/usr/bin/env python3
"""Run with python3 server.py; bind only to loopback for classroom use."""
import argparse
import json
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from engine import ROOT
from service import Service
from chat import ask, config, ChatError


def create_server(port=8765, service=None):
    service = service or Service(ROOT / 'local-state' / 'state.json')
    csrf = secrets.token_urlsafe(24)
    chat_lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def respond(self, status, payload, mime='application/json'):
            content = json.dumps(payload).encode() if mime == 'application/json' else payload
            self.send_response(status)
            self.send_header('Content-Type', mime + '; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(content)

        def allowed_host(self):
            return self.headers.get('Host') in [f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}']

        def do_GET(self):
            if not self.allowed_host():
                return self.respond(403, {'error': 'Use the localhost URL.'})
            url = urlparse(self.path)
            try:
                if url.path == '/api/health':
                    cfg = config()
                    return self.respond(200, {'ok': True, 'api_key_configured': bool(cfg['OPENAI_API_KEY']),
                                              'model': cfg['OPENAI_MODEL'], 'csrf': csrf})
                if url.path == '/api/dashboard':
                    return self.respond(200, service.engine.dashboard(service.snapshot()))
                if url.path == '/api/sku':
                    return self.respond(200, service.engine.plan(parse_qs(url.query).get('sku', [''])[0], service.snapshot(), True))
                if url.path == '/api/anomalies':
                    return self.respond(200, service.engine.anomalies())
                if url.path == '/api/audit':
                    return self.respond(200, service.snapshot()['audit'])
                static = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}
                if url.path in static:
                    filename, mime = static[url.path]
                    return self.respond(200, (ROOT / 'static' / filename).read_bytes(), mime)
                self.respond(404, {'error': 'Not found'})
            except (ValueError, KeyError) as exc:
                self.respond(400, {'error': str(exc)})

        def do_POST(self):
            if not self.allowed_host() or self.headers.get('X-CSRF-Token') != csrf:
                return self.respond(403, {'error': 'Reload the local app before changing data.'})
            origin = self.headers.get('Origin')
            if origin and origin not in [f'http://localhost:{self.server.server_port}', f'http://127.0.0.1:{self.server.server_port}']:
                return self.respond(403, {'error': 'Origin not allowed.'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 200000:
                    raise ValueError('Invalid request size.')
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError('Expected a JSON object.')
                if self.path == '/api/preview-stage':
                    result = service.preview_stage(body['stage'])
                elif self.path == '/api/preview-delay':
                    result = service.preview_delay(body['sku'], body['delay_days'])
                elif self.path == '/api/apply':
                    result = service.apply(body['id'])
                elif self.path == '/api/chat':
                    if not chat_lock.acquire(blocking=False):
                        return self.respond(409, {'error': 'A chatbot request is already running. Wait for it to finish.'})
                    try:
                        result = ask(service, body['message'], body.get('history'))
                    finally:
                        chat_lock.release()
                else:
                    return self.respond(404, {'error': 'Not found'})
                self.respond(200, result)
            except ChatError as exc:
                self.respond(502, {'error': str(exc)})
            except (ValueError, KeyError, TypeError) as exc:
                self.respond(400, {'error': str(exc)})

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = create_server(args.port)
    print(f'Case 2 reference app: http://127.0.0.1:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
