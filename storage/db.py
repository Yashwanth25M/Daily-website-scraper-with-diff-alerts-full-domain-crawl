import sqlite3

conn = sqlite3.connect("snapshots.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS snapshots (
    url TEXT,
    content_hash TEXT,
    text TEXT,
    run_id TEXT
)
""")
conn.commit()

def fetch_recent_runs(limit=5):
    cur.execute("""
        SELECT DISTINCT run_id
        FROM snapshots
        ORDER BY run_id DESC
        LIMIT ?
    """, (limit,))
    return [r[0] for r in cur.fetchall()]

def save_snapshot(url, h, text, run_id):
    cur.execute(
        "INSERT INTO snapshots VALUES (?, ?, ?, ?)",
        (url, h, text, run_id)
    )
    conn.commit()


def fetch_last_two_runs():
    cur.execute("""
    SELECT DISTINCT run_id
    FROM snapshots
    ORDER BY run_id DESC
    LIMIT 2
    """)
    return [r[0] for r in cur.fetchall()]


def fetch_hashes_by_run(run_id):
    cur.execute(
        "SELECT url, content_hash FROM snapshots WHERE run_id = ?",
        (run_id,)
    )
    return dict(cur.fetchall())


def fetch_texts_by_run(run_id):
    cur.execute(
        "SELECT url, text FROM snapshots WHERE run_id = ?",
        (run_id,)
    )
    return dict(cur.fetchall())

def fetch_recent_runs_with_counts(limit=5):
    cur.execute("""
    SELECT run_id
    FROM (
        SELECT DISTINCT run_id
        FROM snapshots
        ORDER BY run_id DESC
        LIMIT ?
    )
    ORDER BY run_id ASC
    """, (limit,))
    return [r[0] for r in cur.fetchall()]

