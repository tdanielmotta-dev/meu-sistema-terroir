import sqlite3
from pathlib import Path

DB_PATH = Path("wineindex.db")


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
        subregion TEXT,
        country TEXT,
        denomination TEXT,
        classification TEXT,
        wine_type TEXT,
        alcohol TEXT,
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
        denomination TEXT,
        classification TEXT,
        allowed_grapes TEXT,
        min_alcohol TEXT,
        aging_rules TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()


def seed_if_empty():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS n FROM wines")
    wines_count = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) AS n FROM denominations")
    den_count = cur.fetchone()["n"]

    if wines_count == 0:
        wines_seed = [
            (
                "Gato Negro", "Malbec", "2019", "Malbec", "Central Valley", "",
                "Chile", "", "", "Tinto", "13%", "frutas vermelhas, ameixa",
                "frutado, macio, médio corpo", "média", "médio", "",
                "mediterrâneo", "", "", "massas, carnes leves", "Seed inicial"
            ),
            (
                "Moët & Chandon", "Dom Pérignon", "2013", "Chardonnay, Pinot Noir",
                "Champagne", "", "França", "Champagne AOC", "AOC", "Espumante",
                "12.5%", "cítricos, brioche, flores brancas", "cremoso, tenso, mineral",
                "alta", "médio", "calcário", "frio continental", "champenois",
                "sur lies prolongado", "frutos do mar, alta gastronomia", "Seed inicial"
            ),
        ]

        cur.executemany("""
        INSERT INTO wines (
            producer, wine_name, vintage, grape, region, subregion, country,
            denomination, classification, wine_type, alcohol, aromas, palate,
            acidity, body, soil, climate, terroir, aging, pairing, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, wines_seed)

    if den_count == 0:
        den_seed = [
            (
                "França",
                "Champagne",
                "Champagne AOC",
                "AOC",
                "Chardonnay, Pinot Noir, Pinot Meunier",
                "11%",
                "Conforme regras da appellation",
                "Denominação clássica de Champagne"
            ),
            (
                "Itália",
                "Piemonte",
                "Barolo DOCG",
                "DOCG",
                "Nebbiolo",
                "13%",
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


def insert_or_update_wine(record: dict):
    conn = get_connection()
    cur = conn.cursor()

    producer = record.get("producer", "")
    wine_name = record.get("wine_name", "")
    vintage = record.get("vintage", "")

    cur.execute("""
        SELECT id FROM wines
        WHERE lower(coalesce(producer,'')) = lower(?)
          AND lower(coalesce(wine_name,'')) = lower(?)
          AND lower(coalesce(vintage,'')) = lower(?)
        LIMIT 1
    """, (producer, wine_name, vintage))

    existing = cur.fetchone()

    fields = [
        "producer", "wine_name", "vintage", "grape", "region", "subregion", "country",
        "denomination", "classification", "wine_type", "alcohol", "aromas", "palate",
        "acidity", "body", "soil", "climate", "terroir", "aging", "pairing", "notes"
    ]

    values = [record.get(f, "") for f in fields]

    if existing:
        wine_id = existing["id"]
        set_clause = ", ".join([f"{f}=?" for f in fields])
        cur.execute(f"UPDATE wines SET {set_clause} WHERE id=?", values + [wine_id])
    else:
        placeholders = ",".join(["?"] * len(fields))
        cur.execute(f"""
            INSERT INTO wines ({",".join(fields)})
            VALUES ({placeholders})
        """, values)

    conn.commit()
    conn.close()
