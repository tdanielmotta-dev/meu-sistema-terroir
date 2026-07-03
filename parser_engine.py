import re

GRAPES = [
    "Merlot", "Cabernet Sauvignon", "Cabernet Franc", "Chardonnay",
    "Pinot Noir", "Sauvignon Blanc", "Riesling", "Syrah", "Shiraz",
    "Malbec", "Nebbiolo", "Sangiovese", "Tempranillo", "Carménère",
    "Carmenere", "Touriga Nacional", "Semillon", "Sémillon",
    "Petit Verdot", "Barbera", "Dolcetto", "Grenache", "Garnacha",
    "Pinot Grigio", "Moscato", "Gewurztraminer", "Viognier"
]

COUNTRIES = [
    "Chile", "França", "France", "Itália", "Italia", "Spain", "Espanha",
    "Portugal", "Argentina", "Brasil", "Germany", "Alemanha",
    "United States", "USA", "Estados Unidos", "South Africa",
    "África do Sul", "New Zealand", "Nova Zelândia", "Australia", "Austrália"
]

REGIONS = [
    "Valle Central", "Maipo", "Colchagua", "Casablanca", "Maule",
    "Bordeaux", "Bourgogne", "Champagne", "Rhône", "Loire", "Alsace",
    "Piemonte", "Toscana", "Barolo", "Barbaresco", "Chianti",
    "Rioja", "Ribera del Duero", "Priorat", "Douro", "Dão",
    "Mosel", "Rheingau", "Mendoza", "Napa Valley", "Sonoma",
    "Marlborough", "Stellenbosch"
]

DENOMINATIONS = [
    "DOCG", "DOC", "AOC", "AOP", "IGP", "DOP", "IGT", "DO", "DOCa"
]


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def find_first_keyword(text: str, keywords: list):
    low = (text or "").lower()
    for item in keywords:
        if item.lower() in low:
            return item
    return None


def parse_wine_query(query: str):
    query = normalize_spaces(query)
    tokens = query.split()

    vintage = None
    m = re.search(r"\b(19\d{2}|20\d{2})\b", query)
    if m:
        vintage = m.group(1)

    grape = find_first_keyword(query, GRAPES)
    country = find_first_keyword(query, COUNTRIES)
    region = find_first_keyword(query, REGIONS)
    denomination = find_first_keyword(query, DENOMINATIONS)

    return {
        "normalized_query": query,
        "tokens": tokens,
        "vintage": vintage,
        "grape": grape,
        "country": country,
        "region":region,
      "denomination": denomination
    }
