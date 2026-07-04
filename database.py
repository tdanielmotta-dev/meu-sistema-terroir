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
                "Gato Negro", "Malbec", "2019", "Malbec", "Central Valley", "", "Chile",
                "", "", "Tinto", 13.0,
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
                "Château Exemplo", "Merlot Reserva", "2020", "Merlot", "Bordeaux", "", "França",
                "Bordeaux AOC", "AOC", "Tinto", 13.5,
                "frutas negras, cassis",
                "taninos médios, final seco",
                "média",
                "médio",
                "argilo-calcário",
                "temperado marítimo",
                "margem esquerda clássica",
                "carvalho francês",
                "carnes e queijos",
                "Exemplo inicial de vinho no banco"
            ),
            (
                "Cantina Exemplo", "Barolo Classico", "2018", "Nebbiolo", "Piemonte", "Barolo", "Itália",
                "Barolo DOCG", "DOCG", "Tinto", 14.0,
                "rosa, alcatrão, cereja",
                "estruturado, tânico, longo",
                "alta",
                "encorpado",
                "margas calcárias",
                "continental",
                "colinas de Barolo",
                "envelhecimento prolongado",
                "carnes de caça, risoto",
                "Exemplo inicial de vinho no banco"
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
                "França", "Bordeaux", "", "Bordeaux AOC", "AOC",
                "Merlot, Cabernet Sauvignon, Cabernet Franc",
                10.5,
                "Variável conforme subzona e estilo",
                "argilo-calcário e cascalho",
                "temperado marítimo",
                "grande mosaico de terroirs bordaleses",
                "Denominação genérica de Bordeaux"
            ),
            (
                "Itália", "Piemonte", "Barolo", "Barolo DOCG", "DOCG",
                "Nebbiolo",
                13.0,
                "Maturação obrigatória conforme regra da DOCG",
                "margas calcárias",
                "continental",
                "colinas de Barolo",
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
