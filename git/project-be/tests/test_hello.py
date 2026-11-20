"""ADR-006 acceptance criteria 1 to 3, with a stub in place of the database."""
import json
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from hello.app import DatabaseUnavailable, make_server

ORIGIN = "http://localhost:47101"


class Endpoint(unittest.TestCase):
    def start(self, greeting):
        server = make_server(0, greeting, ORIGIN)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return f"http://127.0.0.1:{server.server_address[1]}"

    def get(self, url, origin=None):
        request = urllib.request.Request(url, headers={"Origin": origin} if origin else {})
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.headers, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, error.headers, json.loads(error.read())

    def test_200_with_the_greeting(self):
        status, _, body = self.get(self.start(lambda: "Hello, World!") + "/api/hello")
        self.assertEqual((status, body), (200, {"message": "Hello, World!"}))

    def test_503_when_the_database_is_down(self):
        def down():
            raise DatabaseUnavailable

        status, _, body = self.get(self.start(down) + "/api/hello")
        self.assertEqual((status, body), (503, {"error": "database unavailable"}))

    def test_404_elsewhere(self):
        status, _, _ = self.get(self.start(lambda: "hi") + "/api/other")
        self.assertEqual(status, 404)

    def test_cors_allows_only_the_web_app(self):
        base = self.start(lambda: "hi")
        _, allowed, _ = self.get(base + "/api/hello", ORIGIN)
        _, other, _ = self.get(base + "/api/hello", "http://evil.test")
        self.assertEqual(allowed["Access-Control-Allow-Origin"], ORIGIN)
        self.assertIsNone(other["Access-Control-Allow-Origin"])


class Budget(unittest.TestCase):
    def test_the_only_runtime_dependency_is_psycopg(self):  # ADR-004 law 3, ADR-006 law 2
        lines = (Path(__file__).parents[1] / "requirements.txt").read_text(encoding="utf-8").splitlines()
        names = [line.split("[")[0].split("=")[0].split(">")[0].strip() for line in lines
                 if line.strip() and not line.startswith("#")]
        self.assertEqual(names, ["psycopg"])


if __name__ == "__main__":
    unittest.main()
