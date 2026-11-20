"""The endpoint and its contract (ADR-006 law 1), on the standard library's http.server."""
from __future__ import annotations

import json
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PATH = "/api/hello"


class DatabaseUnavailable(Exception):
    """The greeting could not be read."""


def read_greeting(database_url: str) -> str:
    """Read the one greeting row, as the read-only role (ADR-005 law 4)."""
    import psycopg  # the only runtime dependency

    try:
        with psycopg.connect(database_url, connect_timeout=3) as conn:
            row = conn.execute("SELECT message FROM greeting WHERE id = 1").fetchone()
    except psycopg.Error as error:
        raise DatabaseUnavailable from error
    if row is None:
        raise DatabaseUnavailable("no greeting row")
    return row[0]


def make_server(port: int, greeting: Callable[[], str], allowed_origin: str) -> ThreadingHTTPServer:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 (http.server's naming)
            if self.path != PATH:
                return self.reply(404, {"error": "not found"})
            try:
                return self.reply(200, {"message": greeting()})
            except DatabaseUnavailable:
                return self.reply(503, {"error": "database unavailable"})

        def reply(self, status: int, body: dict) -> None:
            data = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            if self.headers.get("Origin") == allowed_origin:  # ADR-006 law 3: one origin only
                self.send_header("Access-Control-Allow-Origin", allowed_origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, fmt: str, *args) -> None:
            print(f"{self.address_string()} {fmt % args}")

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)
