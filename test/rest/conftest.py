import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

MAPPINGS = [
    {
        "method": "GET",
        "url": "/calc/sqrt/64",
        "status": 200,
        "body": "8",
        "headers": {"Content-Type": "text/plain", "Access-Control-Allow-Origin": "*"},
    }
]


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        for mapping in MAPPINGS:
            if mapping["method"] == "GET" and mapping["url"] == self.path:
                self.send_response(mapping["status"])
                for k, v in mapping["headers"].items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(mapping["body"].encode())
                return
        self.send_response(404)
        self.end_headers()


@pytest.fixture(scope="session", autouse=True)
def mock_server():
    server = HTTPServer(("localhost", 9090), MockHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield server
    server.shutdown()
