#!/bin/sh
# ADR-005 law 4: the API connects as hello_api, which can only read greeting.
# A shell script, so the password comes from the environment (.env), never from Git.
set -e
psql -v ON_ERROR_STOP=1 -v pw="$API_DB_PASSWORD" -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<'SQL'
CREATE ROLE hello_api LOGIN PASSWORD :'pw';
GRANT CONNECT ON DATABASE hello TO hello_api;
GRANT USAGE ON SCHEMA public TO hello_api;
GRANT SELECT ON greeting TO hello_api;
SQL
