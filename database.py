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
        subregion TEXT,
        country TEXT,
        denomination TEXT,
        classification TEXT,
        wine_type TEXT,
        alcohol REAL,
        aromas TEXT,
        palate TEXT,
        acidity TEXT,
        body TEXT,
        soil TEXT,
        climate TEXT,
        terroir TEXT,
        aging TEXT,
        pairing TEXT,
        notes TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS denominations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT,
        region TEXT,
        subregion TEXT,
        denomination TEXT,
        classification TEXT,
        allowed_grapes TEXT,
        min_alcohol REAL,
        aging_rules TEXT,
        soil TEXT,
        climate TEXT,
        terroir TEXT,
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
                "Gato Negro",
                "Malbec",
                "2019",
                "Malbec",
                "Central Valley",
                "",
                "Chile",
                "DO",
                "",
                "Tinto",
                13.0,
                "frutas vermelhas, ameixa",
                "frutado, macio, médio corpo",
                "média",
                "médio",
                "",
                "mediterrâneo",
                "",
                "",
                "",
                "Seed inicial"
            ),
            (
                "Château Exemplo",
                "Merlot Reserva",
                "2020",
                "Merlot",
                "Bordeaux",
                "",
                "França",
                "Bordeaux AOC",
                "AOC",
                "Tinto",
                13.5,
                "ameixa, cassis",
                "estruturado, elegante",
                "média",
                "médio+",
                "argilo-calcário",
                "temperado marítimo",
                "cascalho e argila",
                "carvalho francês",
                "carnes assadas",
                "Exemplo inicial"
            ),
            (
                "Cantina Exemplo",
                "Barolo Classico",
                "2018",
                "Nebbiolo",
                "Piemonte",
                "Barolo",
                "Itália",
                "Barolo DOCG",
                "DOCG",
                "Tinto",
                14.0,
                "rosas, alcatrão, cereja",
                "tânico, complexo, longo",
                "alta",
                "encorpado",
                "marga calcária",
                "continental",
                "encostas e solos calcários",
                "maturação longa obrigatória",
                "caça, risotos, cordeiro",
                "Exemplo inicial"
            ),
        ]

        cur.executemany("""
        INSERT INTO wines (
            producer, wine_name, vintage, grape, region, subregion, country,
            denomination, classification, wine_type, alcohol,
            aromas, palate, acidity, body, soil, climate, terroir,
            aging, pairing, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, wines_seed)

    if den_count == 0:
        den_seed = [
            (
                "Chile",
                "Central Valley",
                "",
                "DO",
                "",
                "Malbec, Cabernet Sauvignon, Merlot, Carmenere, Syrah",
                11.5,
                "",
                "",
                "mediterrâneo",
                "",
                "Denominação genérica simplificada para seed"
            ),
            (
                "França",
                "Bordeaux",
                "",
                "Bordeaux AOC",
                "AOC",
                "Merlot, Cabernet Sauvignon, Cabernet Franc",
                10.5,
                "Variável conforme estilo/subzona",
                "argilo-calcário, cascalho",
                "temperado marítimo",
                "cascalho, argila, calcário",
                "Denominação genérica de Bordeaux"
            ),
            (
                "Itália",
                "Piemonte",
                "Barolo",
                "Barolo DOCG",
                "DOCG",
                "Nebbiolo",
                13.0,
                "Maturação obrigatória conforme regra da DOCG",
                "marga calcária",
                "continental",
                "encostas e solos calcários",
                "Denominação clássica do Piemonte"
            ),
        ]

        cur.executemany("""
        INSERT INTO denominations (
            country, region, subregion, denomination, classification,
            allowed_grapes, min_alcohol, aging_rules, soil, climate, terroir, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
