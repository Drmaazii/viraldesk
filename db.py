"""ViralDesk storage layer — Turso (libsql) when configured, local SQLite otherwise.

Remote: set TURSO_URL (libsql://...) and TURSO_TOKEN env vars. On Streamlit
Cloud these come from st.secrets, which app.py copies into env at startup.
The radar cron on Muse's machine sets them too, so scheduled runs write
straight to the cloud DB.

Local: falls back to plain sqlite3 on viraldesk.db next to this file — the
radar cron, preview studio and production pipelines keep working with zero
config. No libsql install needed for local use.
"""
import json
import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = __file__.replace("db.py", "viraldesk.db")


def remote_config():
    """(url, token) when a remote Turso DB is configured, else None."""
    url = os.environ.get("TURSO_URL", "").strip()
    token = os.environ.get("TURSO_TOKEN", "").strip()
    return (url, token) if url and token else None


def using_remote():
    return remote_config() is not None


def connect():
    """A DBAPI connection: remote Turso when configured, else local sqlite3."""
    cfg = remote_config()
    if cfg:
        import libsql  # only needed for remote; local fallback needs nothing new

        url, token = cfg
        return libsql.connect(database=url, auth_token=token)
    return sqlite3.connect(DB_PATH)


def dicts(cur):
    """Cursor rows -> list of dicts. Works on sqlite3 and libsql cursors."""
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def exec_script(conn, sql):
    """Run a multi-statement SQL script one statement at a time.

    Avoids executescript(), whose availability differs between drivers.
    """
    for stmt in sql.split(";"):
        s = stmt.strip()
        if s:
            conn.execute(s)


def init_db():
    c = connect()
    exec_script(
        c,
        """
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            canonical_url TEXT,
            platform TEXT,
            author TEXT,
            post_date TEXT,
            caption TEXT,
            views INTEGER,
            likes INTEGER,
            comments INTEGER,
            shares INTEGER,
            transcript TEXT,
            description TEXT,
            niche_tags TEXT DEFAULT '',
            fetch_status TEXT DEFAULT 'pending',
            fetch_error TEXT DEFAULT '',
            fetched_at TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link_id INTEGER NOT NULL REFERENCES links(id),
            version INTEGER NOT NULL,
            title TEXT,
            analysis_json TEXT NOT NULL,
            master_prompt TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(link_id, version)
        );
        CREATE INDEX IF NOT EXISTS idx_links_platform ON links(platform);
        CREATE INDEX IF NOT EXISTS idx_prompts_link ON prompts(link_id);
        """,
    )
    c.commit()
    c.close()


def init_trends_tables():
    """Trend Radar tables. Same schema the radar has always used."""
    c = connect()
    exec_script(
        c,
        """
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            niche TEXT NOT NULL,
            kind TEXT NOT NULL DEFAULT 'blog_topic',
            source TEXT NOT NULL,
            source_url TEXT DEFAULT '',
            score REAL NOT NULL DEFAULT 0,
            velocity REAL NOT NULL DEFAULT 0,
            engagement REAL NOT NULL DEFAULT 0,
            freshness REAL NOT NULL DEFAULT 0,
            fetched_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'new',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS trend_decodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trend_id INTEGER NOT NULL REFERENCES trends(id),
            kind TEXT NOT NULL,
            link_id INTEGER,
            prompt_id INTEGER,
            title TEXT,
            analysis_json TEXT NOT NULL,
            master_prompt TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_trends_niche ON trends(niche);
        CREATE INDEX IF NOT EXISTS idx_trends_status ON trends(status);
        CREATE INDEX IF NOT EXISTS idx_decodes_trend ON trend_decodes(trend_id);
        CREATE INDEX IF NOT EXISTS idx_decodes_kind ON trend_decodes(kind);
        CREATE INDEX IF NOT EXISTS idx_trends_niche_kind ON trends(niche, kind);
        """,
    )
    # migration for DBs created before the kind column existed
    try:
        c.execute("ALTER TABLE trends ADD COLUMN kind TEXT NOT NULL DEFAULT 'blog_topic'")
    except Exception:
        pass  # column already there
    c.commit()
    c.close()


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_link(rec: dict) -> int:
    rec = dict(rec)
    rec.setdefault("created_at", now_iso())
    rec.setdefault("fetched_at", now_iso())
    cols = [
        "url", "canonical_url", "platform", "author", "post_date", "caption",
        "views", "likes", "comments", "shares", "transcript", "description",
        "niche_tags", "fetch_status", "fetch_error", "fetched_at", "created_at",
    ]
    c = connect()
    cur = c.execute(
        f"INSERT INTO links ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",
        [rec.get(k) for k in cols],
    )
    c.commit()
    lid = cur.lastrowid
    c.close()
    return lid


def list_links(limit=100, search=""):
    c = connect()
    if search:
        q = """SELECT * FROM links
               WHERE url LIKE ? OR caption LIKE ? OR author LIKE ?
                  OR niche_tags LIKE ? OR platform LIKE ?
               ORDER BY id DESC LIMIT ?"""
        s = f"%{search}%"
        rows = dicts(c.execute(q, (s, s, s, s, s, limit)))
    else:
        rows = dicts(c.execute("SELECT * FROM links ORDER BY id DESC LIMIT ?", (limit,)))
    c.close()
    return rows


def get_link(link_id: int):
    c = connect()
    rows = dicts(c.execute("SELECT * FROM links WHERE id=?", (link_id,)))
    c.close()
    return rows[0] if rows else None


def save_prompt(link_id: int, title: str, analysis: dict, master_prompt: str) -> int:
    c = connect()
    row = dicts(
        c.execute("SELECT COALESCE(MAX(version),0) AS v FROM prompts WHERE link_id=?", (link_id,))
    )[0]
    version = (row["v"] or 0) + 1
    cur = c.execute(
        "INSERT INTO prompts (link_id, version, title, analysis_json, master_prompt, created_at)"
        " VALUES (?,?,?,?,?,?)",
        (link_id, version, title, json.dumps(analysis, ensure_ascii=False), master_prompt, now_iso()),
    )
    c.commit()
    pid = cur.lastrowid
    c.close()
    return pid


def list_prompts():
    c = connect()
    rows = dicts(
        c.execute(
            """SELECT p.*, l.url AS link_url, l.platform AS link_platform, l.author AS link_author
               FROM prompts p JOIN links l ON l.id = p.link_id
               ORDER BY p.id DESC"""
        )
    )
    c.close()
    for d in rows:
        d["analysis"] = json.loads(d["analysis_json"])
    return rows


def prompt_versions(link_id: int):
    c = connect()
    rows = dicts(
        c.execute("SELECT * FROM prompts WHERE link_id=? ORDER BY version DESC", (link_id,))
    )
    c.close()
    for d in rows:
        d["analysis"] = json.loads(d["analysis_json"])
    return rows


def get_niche_items(niche):
    """All decoded trend items for a niche: blog topics + videos with decodes."""
    c = connect()
    rows = dicts(
        c.execute(
            """SELECT t.*, d.title AS decode_title, d.analysis_json, d.master_prompt,
                      d.link_id, d.prompt_id
               FROM trends t JOIN trend_decodes d ON d.trend_id = t.id
               WHERE t.niche = ?
               ORDER BY t.kind, t.score DESC""",
            (niche,),
        )
    )
    c.close()
    for d in rows:
        d["analysis"] = json.loads(d["analysis_json"])
    return rows
