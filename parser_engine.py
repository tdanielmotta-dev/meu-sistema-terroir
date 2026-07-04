import re

GRAPES = [
    "Cabernet Sauvignon", "Cabernet Franc", "Merlot", "Malbec", "Syrah", "Shiraz",
    "Pinot Noir", "Chardonnay", "Sauvignon Blanc", "Riesling", "Nebbiolo",
    "Sangiovese", "Tempranillo", "Grenache", "Garnacha", "Carmenere", "Carménère",
    "Touriga Nacional", "Gewurztraminer", "Gewürztraminer", "Viognier", "Gamay"
]

COUNTRIES = [
    "França", "Itália", "Espanha", "Portugal", "Chile", "Argentina", "Brasil",
    "Estados Unidos", "Alemanha", "Áustria", "África do Sul"
]

REGIONS = [
    "Champagne", "Bordeaux", "Bourgogne", "Borgonha", "Piemonte", "Toscana",
    "Rioja", "Douro", "Mendoza", "Central Valley", "Chablis", "Barolo", "Barbaresco",
    "Sauternes", "Pomerol", "Margaux", "Napa Valley"
]

DENOMINATIONS = [
    "DOCG", "DOC", "DO", "DOP", "IGP", "AOC", "AOP", "AVA"
]

def parse_wine_query(query: str):
    raw = query or ""
    normalized = " ".join(raw.strip().split())

    tokens = normalized.split()

    vintage = None
    m = re.search(r"\b(19\d{2}|20\d{2}|21\d{2})\b", normalized)
    if m:
        vintage = m.group(1)

    grape = None
    for g in sorted(GRAPES, key=len, reverse=True):
        if g.lower() in normalized.lower():
            grape = g
            break

    country = None
    for c in COUNTRIES:
        if c.lower() in normalized.lower():
            country = c
            break

    region = None
    for r in sorted(REGIONS, key=len, reverse=True):
        if r.lower() in normalized.lower():
            region = r
            break

    denomination = None
    for d in DENOMINATIONS:
        if re.search(rf"\b{re.escape(d)}\b", normalized, flags=re.I):
            denomination = d
            break

    return {
        "raw_query": raw,
        "normalized_query": normalized,
        "tokens": tokens,
        "vintage": vintage,
        "grape": grape,
        "country": country,
        "region": region,
        "subregion": None,
        "denomination": denomination,
    }
