-- ADR-005 law 3: one table, one row, no personal data.
CREATE TABLE greeting (
    id      integer PRIMARY KEY,
    message text    NOT NULL
);

INSERT INTO greeting (id, message) VALUES (1, 'Hello, World!');  -- CFG-002
