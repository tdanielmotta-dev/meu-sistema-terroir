import sqlite3
from pathlib import Path

DB_PATH = Path("wineindex.db")

WINE_FIELDS = [
    "producer",
    "wine_name",
    "vintage",
    "grape",
    "country",
    "region",
    "subregion",
    "denomination",
    "classification",
    "wine_type",
    "alcohol",
    "aromas",
    "palate",
    "acidity",
    "body",
    "soil",
    "climate",
    "terroir",
    "aging",
    "pairing",
    "notes",
]

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
        country TEXT,
        region TEXT,
        subregion TEXT,
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

    conn.commit()
    conn.close()

def seed_if_empty():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM wines")
    count = cur.fetchone()[0]

    if count == 0:
        seed_rows = [
            (
                "Gato Negro",
                "Malbec",
                "2019",
                "Malbec",
                "Chile",
                "Central Valley",
                "",
                "",
                "",
                "Tinto",
                "13%",
                "frutas vermelhas maduras, ameixa",
                "frutado, macio, médio corpo",
                "média",
                "médio",
                "",
                "mediterrâneo",
                "",
                "",
                "massas, carnes leves, pizzas",
                "Seed inicial"
            ),
            (
                "Moët & Chandon",
                "Dom Pérignon",
                "",
                "Chardonnay, Pinot Noir",
                "França",
                "Champagne",
                "",
                "Champagne AOC",
                "Prestige Cuvée",
                "Espumante",
                "12.5%",
                "cítricos, brioche, flores, frutas brancas, tostado",
                "fino, cremoso, mineral, complexo",
                "alta",
                "médio a encorpado",
                "calcário, giz",
                "frio continental",
                "Champagne de solos calcários e clima marginal",
                "longo amadurecimento sobre borras",
                "ostras, caviar, frutos do mar, aves nobres",
                "Seed inicial Dom Pérignon"
            ),
            (
                "Produtor Genérico",
                "Barolo",
                "",
                "Nebbiolo",
                "Itália",
                "Piemonte",
                "Barolo",
                "Barolo DOCG",
                "DOCG",
                "Tinto",
                "14%",
                "rosa, alcatrão, cereja, especiarias",
                "estruturado, taninos firmes, final longo",
                "alta",
                "encorpado",
                "margas calcárias",
                "continental",
                "colinas de Langhe",
                "envelhecimento obrigatório conforme DOCG",
                "carnes assadas, caça, trufas",
                "Seed inicial Barolo"
            ),
        ]

        cur.executemany("""
        INSERT INTO wines (
            producer, wine_name, vintage, grape, country, region, subregion,
            denomination, classification, wine_type, alcohol, aromas, palate,
            acidity, body, soil, climate, terroir, aging, pairing, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_rows)

    conn.commit()
    conn.close()

def fetch_all_wines():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM wines ORDER BY producer, wine_name, vintage")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def insert_wine_if_new(record: dict):
    """
    Salva no banco se houver pelo menos producer ou wine_name.
    Não faz deduplicação perfeita; usa heurística simples.
    """
    if not isinstance(record, dict):
        return False

    producer = (record.get("producer") or "").strip()
    wine_name = (record.get("wine_name") or "").strip()
    vintage = (record.get("vintage") or "").strip()

    if not producer and not wine_name:
        return False

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id FROM wines
    WHERE lower(coalesce(producer,'')) = lower(?)
      AND lower(coalesce(wine_name,'')) = lower(?)
      AND lower(coalesce(vintage,'')) = lower(?)
    LIMIT 1
    """, (producer, wine_name, vintage))

    exists = cur.fetchone()
    if exists:
        conn.close()
        return False

    values = [record.get(field, "") for field in WINE_FIELDS]

    cur.execute(f"""
    INSERT INTO wines ({", ".join(WINE_FIELDS)})
    VALUES ({", ".join(["?"] * len(WINE_FIELDS))})
    """, values)

    conn.commit()
    conn.close()
    return True
