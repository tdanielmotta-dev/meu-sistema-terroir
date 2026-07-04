import re

GRAPES = [
    "Malbec", "Merlot", "Cabernet Sauvignon", "Cabernet Franc", "Pinot Noir",
    "Nebbiolo", "Chardonnay", "Sauvignon Blanc", "Syrah", "Carménère",
    "Tempranillo", "Sangiovese", "Grenache", "Gamay", "Riesling"
]

COUNTRIES = ["França", "Itália", "Chile", "Argentina", "Espanha", "Portugal", "Brasil"]
REGIONS = ["Bordeaux", "Piemonte", "Barolo", "Rioja", "Mendoza", "Central Valley", "Douro", "Champagne"]
DENOMS = ["DOCG", "DOC", "AOC", "DO", "DOP", "IGP", "IG", "AOP"]


def parse_wine_query(query: str):
    query = (query or "").strip()
    tokens = query.split()

    vintage = None
    grape = None
    country = None
    region = None
    subregion = None
    denomination = None

    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", query)
    if year_match:
        vintage = year_match.group(1)

    for g in GRAPES:
        if g.lower() in query.lower():
            grape = g
            break

    for c in COUNTRIES:
        if c.lower() in query.lower():
            country = c
            break

    for r in REGIONS:
        if r.lower() in query.lower():
            region = r
            break

    for d in DENOMS:
        if re.search(rf"\b{re.escape(d)}\b", query, re.IGNORECASE):
            denomination = d
            break

    return {
        "raw_query": query,
        "normalized_query": query.strip(),
        "tokens": tokens,
        "vintage": vintage,
        "grape": grape,
        "country": country,
        "region": region,
        "subregion": subregion,
        "denomination": denomination
    }
