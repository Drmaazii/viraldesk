"""One-shot migration: local viraldesk.db -> Turso cloud DB.

Copies links, prompts, trends and trend_decodes. Idempotent-ish: rows are
matched by id, so re-running only copies what is missing.

Run AFTER the Turso database exists and the app is deployed:

    TURSO_URL='libsql://...' TURSO_TOKEN='...' python migrate_to_turso.py

Never paste the token in chat — Muse will run this for you once you share
the token through the secure link.
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db  # noqa: E402

TABLES = ("links", "prompts", "trends", "trend_decodes")


def main():
    if not db.remote_config():
        print("Set TURSO_URL and TURSO_TOKEN first. Nothing migrated.")
        return 1

    local = sqlite3.connect(db.DB_PATH)
    local.row_factory = sqlite3.Row

    # Creates the same tables on Turso (connect() targets remote now).
    db.init_db()
    db.init_trends_tables()
    remote = db.connect()

    total = 0
    for table in TABLES:
        try:
            rows = [dict(r) for r in local.execute(f"SELECT * FROM {table}")]
        except Exception as e:  # table missing locally — nothing to copy
            print(f"{table}: skipped ({e})")
            continue
        if not rows:
            print(f"{table}: 0 rows locally")
            continue
        cols = list(rows[0].keys())
        copied = 0
        for r in rows:
            exists = remote.execute(
                f"SELECT 1 FROM {table} WHERE id=?", (r["id"],)
            ).fetchone()
            if exists:
                continue
            remote.execute(
                f"INSERT INTO {table} ({','.join(cols)})"
                f" VALUES ({','.join('?' for _ in cols)})",
                [r[c] for c in cols],
            )
            copied += 1
        remote.commit()
        print(f"{table}: {copied} copied, {len(rows) - copied} already there")
        total += copied

    local.close()
    remote.close()
    print(f"Done. {total} rows copied in total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
