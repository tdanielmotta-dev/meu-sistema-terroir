import sqlite3
from pathlib import Path

DB_PATH = Path("wineindex.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS wines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producer TEXT,
        wine_name TEXT,
        vintage TEXT,
        grape TEXT,
        region TEXT,
        country TEXT,
        denomination TEXT,
        wine_type TEXT,
        alcohol REAL,
        notes TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS denominations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT,
        region TEXT,
        denomination TEXT,
        classification TEXT,
        allowed_grapes TEXT,
        min_alcohol REAL,
        aging_rules TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()


def seed_if_empty():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM wines")
    wines_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM denominations")
    den_count = cur.fetchone()[0]

    if wines_count == 0:
        wines_seed = [
            (
                "Château Exemplo",
                "Merlot Reserva",
                "2020",
                "Merlot",
                "Bordeaux",
                "França",
                "Bordeaux AOC",
                "Tinto",
                13.5,
                "Exemplo inicial de vinho no banco"
            ),
            (
                "Cantina Exemplo",
                "Barolo Classico",
                "2018",
                "Nebbiolo",
                "Piemonte",
                "Itália",
                "Barolo DOCG",
                "Tinto",
                14.0,
                "Exemplo inicial de vinho no banco"
            ),
        ]

        cur.executemany("""
        INSERT INTO wines (
            producer, wine_name, vintage, grape, region, country,
            denomination, wine_type, alcohol, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, wines_seed)

    if den_count == 0:
        den_seed = [
            (
                "França",
                "Bordeaux",
                "Bordeaux AOC",
                "AOC",
                "Merlot, Cabernet Sauvignon, Cabernet Franc",
                10.5,
                "Variável conforme subzona e estilo",
                "Denominação genérica de Bordeaux"
            ),
            (
                "Itália",
                "Piemonte",
                "Barolo DOCG",
                "DOCG",
                "Nebbiolo",
                13.0,
                "Maturação obrigatória conforme regra da DOCG",
                "Denominação clássica do Piemonte"
            ),
        ]

        cur.executemany("""
        INSERT INTO denominations (
            country, region, denomination, classification,
            allowed_grapes, min_alcohol, aging_rules, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, den_seed)

    conn.commit()
    conn.close()


def fetch_all_wines():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM wines ORDER BY producer, wine_name")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_all_denominations():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM denominations ORDER BY country, region, denomination")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
