import sqlite3
from pathlib import Path

DB_PATH = Path("/tmp/wineindex.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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
        classification TEXT,
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

    cur.execute("SELECT COUNT(*) AS c FROM wines")
    wines_count = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM denominations")
    den_count = cur.fetchone()["c"]

    if wines_count == 0:
        wines_seed = [
            (
                "Château Margaux",
                "Pavillon Rouge",
                "2015",
                "Cabernet Sauvignon, Merlot, Petit Verdot, Cabernet Franc",
                "Bordeaux",
                "França",
                "Margaux",
                "AOC",
                "Tinto",
                13.5,
                "Segundo vinho de Château Margaux; Médoc, margem esquerda."
            ),
            (
                "Vietti",
                "Castiglione",
                "2019",
                "Nebbiolo",
                "Piemonte",
                "Itália",
                "Barolo",
                "DOCG",
                "Tinto",
                14.0,
                "Barolo clássico com blend de vinhedos do produtor."
            ),
            (
                "Miolo",
                "Lote 43",
                "2020",
                "Merlot, Cabernet Sauvignon",
                "Vale dos Vinhedos",
                "Brasil",
                "Vale dos Vinhedos",
                "D.O.",
                "Tinto",
                14.0,
                "Ícone brasileiro; corte bordalês."
            ),
        ]

        cur.executemany("""
        INSERT INTO wines (
            producer, wine_name, vintage, grape, region, country,
            denomination, classification, wine_type, alcohol, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, wines_seed)

    if den_count == 0:
        den_seed = [
            (
                "França",
                "Bordeaux",
                "Margaux",
                "AOC",
                "Cabernet Sauvignon, Merlot, Cabernet Franc, Petit Verdot, Malbec, Carmenère",
                10.5,
                "Regras variam por estilo e pelo caderno da denominação aplicável",
                "Appellation do Médoc, margem esquerda de Bordeaux."
            ),
            (
                "Itália",
                "Piemonte",
                "Barolo",
                "DOCG",
                "Nebbiolo",
                13.0,
                "Maturação obrigatória conforme disciplinare da DOCG",
                "Denominação clássica do Piemonte."
            ),
            (
                "Brasil",
                "Vale dos Vinhedos",
                "Vale dos Vinhedos",
                "D.O.",
                "Conforme regulamento da D.O. e categoria do vinho",
                None,
                "Conforme regulamento vigente do conselho regulador",
                "Denominação de origem brasileira relevante da Serra Gaúcha."
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
    cur = conn.cursor()
    cur.execute("SELECT * FROM wines ORDER BY producer, wine_name")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_all_denominations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM denominations ORDER BY country, region, denomination")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
