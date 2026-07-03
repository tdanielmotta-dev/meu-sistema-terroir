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
        country TEXT,
        denomination TEXT,
        wine_type TEXT,
        alcohol REAL,
        body TEXT,
        acidity TEXT,
        tannin TEXT,
        oak TEXT,
        aroma TEXT,
        flavor TEXT,
        soil TEXT,
        climate TEXT,
        aging_rules TEXT,
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
        soil TEXT,
        climate TEXT,
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
                "Viña San Pedro",
                "Gato Negro Merlot",
                "2020",
                "Merlot",
                "Valle Central",
                "Chile",
                "IG / indicação geográfica chilena",
                "Tinto",
                13.0,
                "Médio",
                "Média",
                "Macios",
                "Baixa ou discreta",
                "Frutas vermelhas maduras, ameixa, toque herbáceo leve",
                "Frutado, macio, corpo médio, final simples e agradável",
                "Aluvial / variável conforme origem específica",
                "Mediterrâneo com influência de vales centrais chilenos",
                "Sem regra legal de envelhecimento comparável a DOCG/AOC",
                "Rótulo comercial amplamente distribuído"
            ),
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
                "Médio",
                "Média",
                "Médios",
                "Moderada",
                "Frutas negras, cassis, cedro",
                "Estruturado, fruta madura, madeira e especiarias",
                "Argilo-calcário e cascalho",
                "Oceânico / marítimo",
                "Variável conforme subzona e estilo",
                "Exemplo inicial"
            ),
        ]

        cur.executemany("""
        INSERT INTO wines (
            producer, wine_name, vintage, grape, region, country, denomination,
            wine_type, alcohol, body, acidity, tannin, oak, aroma, flavor,
            soil, climate, aging_rules, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, wines_seed)

    if den_count == 0:
        den_seed = [
            (
                "Chile",
                "Valle Central",
                "Indicação geográfica / origem chilena",
                "IG",
                "Merlot, Cabernet Sauvignon, Carmenère, Chardonnay, Sauvignon Blanc e outras",
                None,
                "Sem regra única equivalente a DOCG/AOC para toda a categoria",
                "Aluvial, coluvial e setores com influência andina em várias subzonas",
                "Mediterrâneo, boa insolação, baixa pressão de chuva em várias áreas",
                "Macrodescrição geral do Valle Central chileno"
            ),
            (
                "França",
                "Bordeaux",
                "Bordeaux AOC",
                "AOC",
                "Merlot, Cabernet Sauvignon, Cabernet Franc, Petit Verdot, Malbec, Carménère; brancas conforme estilo",
                10.5,
                "Variável conforme subzona e estilo",
                "Cascalho, argila, calcário, areia",
                "Oceânico / marítimo",
                "Denominação genérica de Bordeaux"
            ),
        ]

        cur.executemany("""
        INSERT INTO denominations (
            country, region, denomination, classification, allowed_grapes,
            min_alcohol, aging_rules, soil, climate, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
