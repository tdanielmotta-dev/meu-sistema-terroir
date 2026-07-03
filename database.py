import sqlite3
from seed_data import SEED_DENOMINATIONS, SEED_WINES

DB_NAME = "wineindex.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS denominations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        universal_id TEXT UNIQUE,
        country TEXT,
        macro_region TEXT,
        sub_region TEXT,
        appellation_name TEXT,
        legal_level TEXT,
        wine_color_scope TEXT,
        alcohol_min REAL,
        allowed_grapes TEXT,
        notes TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS wines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wine_name TEXT,
        producer TEXT,
        country TEXT,
        macro_region TEXT,
        sub_region TEXT,
        appellation_name TEXT,
        vintage TEXT,
        grapes TEXT,
        style TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()

def seed_if_empty():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM denominations")
    if cur.fetchone()[0] == 0:
        for row in SEED_DENOMINATIONS:
            cur.execute("""
            INSERT INTO denominations (
                universal_id, country, macro_region, sub_region,
                appellation_name, legal_level, wine_color_scope,
                alcohol_min, allowed_grapes, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["universal_id"],
                row["country"],
                row["macro_region"],
                row["sub_region"],
                row["appellation_name"],
                row["legal_level"],
                row["wine_color_scope"],
                row["alcohol_min"],
                row["allowed_grapes"],
                row["notes"]
            ))

    cur.execute("SELECT COUNT(*) FROM wines")
    if cur.fetchone()[0] == 0:
        for row in SEED_WINES:
            cur.execute("""
            INSERT INTO wines (
                wine_name, producer, country, macro_region, sub_region,
                appellation_name, vintage, grapes, style, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["wine_name"],
                row["producer"],
                row["country"],
                row["macro_region"],
                row["sub_region"],
                row["appellation_name"],
                row["vintage"],
                row["grapes"],
                row["style"],
                row["notes"]
            ))

    conn.commit()
    conn.close()

def fetch_all_wines():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT wine_name, producer, country, macro_region, sub_region,
               appellation_name, vintage, grapes, style, notes
        FROM wines
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_all_denominations():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT universal_id, country, macro_region, sub_region,
               appellation_name, legal_level, wine_color_scope,
               alcohol_min, allowed_grapes, notes
        FROM denominations
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
