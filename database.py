import sqlite3
from datetime import datetime

DB_NAME = "wineindex.db"


def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS denominations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        universal_id TEXT UNIQUE NOT NULL,
        country TEXT NOT NULL,
        macro_region TEXT,
        sub_region TEXT NOT NULL,
        appellation_name TEXT NOT NULL,
        legal_level TEXT,
        wine_color_scope TEXT,
        alcohol_min REAL,
        alcohol_max REAL,
        vintage_max INTEGER,
        allowed_grapes TEXT,
        notes TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def seed_if_empty():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM denominations")
    total = cur.fetchone()[0]

    if total == 0:
        from seed_data import SEED_ROWS
        now = datetime.utcnow().isoformat()

        rows = [row + (now, now) for row in SEED_ROWS]

        cur.executemany("""
        INSERT OR IGNORE INTO denominations (
            universal_id,
            country,
            macro_region,
            sub_region,
            appellation_name,
            legal_level,
            wine_color_scope,
            alcohol_min,
            alcohol_max,
            vintage_max,
            allowed_grapes,
            notes,
            created_at,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)

    conn.commit()
    conn.close()


def get_all_denominations():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            universal_id,
            country,
            macro_region,
            sub_region,
            appellation_name,
            legal_level,
            wine_color_scope,
            alcohol_min,
            alcohol_max,
            vintage_max,
            allowed_grapes,
            notes
        FROM denominations
        ORDER BY country, macro_region, sub_region, appellation_name
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def get_appellation_by_name(appellation_name):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            universal_id,
            country,
            macro_region,
            sub_region,
            appellation_name,
            legal_level,
            wine_color_scope,
            alcohol_min,
            alcohol_max,
            vintage_max,
            allowed_grapes,
            notes
        FROM denominations
        WHERE appellation_name = ?
        LIMIT 1
    """, (appellation_name,))

    row = cur.fetchone()
    conn.close()
    return row
