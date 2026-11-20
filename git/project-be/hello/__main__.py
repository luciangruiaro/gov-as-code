"""Start the API: py -3.12 -m hello (ADR-006 law 2). Configuration comes from the environment, or from .env."""
from __future__ import annotations

import os
from pathlib import Path

from hello.app import make_server, read_greeting


def load_env(path: Path) -> None:
    """Fill missing environment variables from KEY=VALUE lines. The process environment wins."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and key and not key.startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    load_env(Path.cwd() / ".env")
    url = os.environ["DATABASE_URL"]
    port = int(os.environ.get("PORT", "47102"))
    origin = os.environ.get("ALLOWED_ORIGIN", "http://localhost:47101")
    server = make_server(port, lambda: read_greeting(url), origin)
    print(f"Hello World API on http://127.0.0.1:{port}/api/hello (allowed origin: {origin})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
