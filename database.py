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
        alcohol REAL,
        climate TEXT,
        soil TEXT,
        terroir TEXT,
        acidity TEXT,
        body TEXT,
        tannins TEXT,
        aging TEXT,
        aromas TEXT,
        palate TEXT,
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
        climate TEXT,
        soil TEXT,
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
                "Château Exemplo",
                "Merlot Reserva",
                "2020",
                "Merlot",
                "Bordeaux",
                "Médoc",
                "França",
                "Bordeaux AOC",
                "AOC",
                "Tinto",
                13.5,
                "Marítimo temperado",
                "Argilo-calcário com cascalho",
                "Margem esquerda de Bordeaux com influência atlântica",
                "Média",
                "Médio",
                "Médios",
                "Barrica parcial",
                "frutas negras, ameixa, cassis, baunilha",
                "frutado, médio corpo, final equilibrado",
                "carnes, queijos curados",
                "Exemplo inicial de vinho no banco"
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
                "Continental",
                "Marga calcária",
                "Encostas do Piemonte com forte expressão de nebbiolo",
                "Alta",
                "Encorpado",
                "Altos",
                "Longo amadurecimento obrigatório",
                "rosa, alcatrão, cereja, especiarias",
                "taninos firmes, alta persistência",
                "caça, carnes braseadas, trufas",
                "Exemplo inicial de vinho no banco"
            ),
        ]

        cur.executemany("""
        INSERT INTO wines (
            producer, wine_name, vintage, grape, region, subregion, country,
            denomination, classification, wine_type, alcohol,
            climate, soil, terroir, acidity, body, tannins, aging,
            aromas, palate, pairing, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, wines_seed)

    if den_count == 0:
        den_seed = [
            (
                "França",
                "Bordeaux",
                "Médoc",
                "Bordeaux AOC",
                "AOC",
                "Merlot, Cabernet Sauvignon, Cabernet Franc",
                10.5,
                "Variável conforme subzona e estilo",
                "Marítimo",
                "Cascalho, argila, calcário",
                "Atlântico, rios e mosaico de solos",
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
                "Continental",
                "Marga calcária",
                "Colinas do Langhe",
                "Denominação clássica do Piemonte"
            ),
        ]

        cur.executemany("""
        INSERT INTO denominations (
            country, region, subregion, denomination, classification,
            allowed_grapes, min_alcohol, aging_rules, climate, soil, terroir, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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


def save_online_result_to_db(final_profile: dict):
    """
    Salva resultado consolidado no banco se tiver informação mínima útil.
    """
    if not final_profile:
        return

    producer = final_profile.get("producer", "") or ""
    wine_name = final_profile.get("wine_name", "") or ""
    denomination = final_profile.get("denomination", "") or ""

    # Só salva se pelo menos um núcleo estiver preenchido
    if not any([producer.strip(), wine_name.strip(), denomination.strip()]):
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO wines (
        producer, wine_name, vintage, grape, region, subregion, country,
        denomination, classification, wine_type, alcohol,
        climate, soil, terroir, acidity, body, tannins, aging,
        aromas, palate, pairing, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        final_profile.get("producer"),
        final_profile.get("wine_name"),
        final_profile.get("vintage"),
        final_profile.get("grape"),
        final_profile.get("region"),
        final_profile.get("subregion"),
        final_profile.get("country"),
        final_profile.get("denomination"),
        final_profile.get("classification"),
        final_profile.get("wine_type"),
        _to_float(final_profile.get("alcohol")),
        final_profile.get("climate"),
        final_profile.get("soil"),
        final_profile.get("terroir"),
        final_profile.get("acidity"),
        final_profile.get("body"),
        final_profile.get("tannins"),
        final_profile.get("aging"),
        final_profile.get("aromas"),
        final_profile.get("palate"),
        final_profile.get("pairing"),
        final_profile.get("notes"),
    ))

    conn.commit()
    conn.close()


def _to_float(value):
    if value is None:
        return None
    try:
        if isinstance(value, str):
            value = value.replace("%", "").replace(",", ".").strip()
        return float(value)
    except Exception:
        return None
