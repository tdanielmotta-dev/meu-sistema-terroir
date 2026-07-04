import re

KNOWN_GRAPES = [
    "cabernet sauvignon", "cabernet franc", "merlot", "malbec", "pinot noir",
    "syrah", "shiraz", "nebbiolo", "sangiovese", "tempranillo", "carmenere",
    "chardonnay", "sauvignon blanc", "riesling", "gewurztraminer", "chenin blanc",
    "viognier", "grenache", "garnacha", "touriga nacional", "aragonez", "tannat"
]

KNOWN_COUNTRIES = [
    "frança", "italia", "itália", "espanha", "portugal", "chile", "argentina",
    "brasil", "uruguai", "alemanha", "australia", "austrália", "estados unidos"
]

KNOWN_REGIONS = [
    "bordeaux", "bourgogne", "burgundy", "champagne", "piemonte", "toscana",
    "rioja", "douro", "central valley", "mendoza", "barolo", "barbaresco",
    "chablis", "sauternes", "medoc", "médoc"
]

KNOWN_DENOMINATIONS = [
    "aoc", "doc", "docg", "dop", "igp", "igt", "do", "vt"
]


def parse_wine_query(query: str):
    raw = (query or "").strip()
    normalized = " ".join(raw.split())

    tokens = normalized.split()
    vintage = None
    grape = None
    country = None
    region = None
    subregion = None
    denomination = None

    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", normalized)
    if year_match:
        vintage = year_match.group(1)

    lower = normalized.lower()

    for g in sorted(KNOWN_GRAPES, key=len, reverse=True):
        if g in lower:
            grape = g.title()
            break

    for c in sorted(KNOWN_COUNTRIES, key=len, reverse=True):
        if c in lower:
            country = c.title()
            break

    for r in sorted(KNOWN_REGIONS, key=len, reverse=True):
        if r in lower:
            region = r.title()
            break

    for d in sorted(KNOWN_DENOMINATIONS, key=len, reverse=True):
        if re.search(rf"\b{re.escape(d)}\b", lower):
            denomination = d.upper()
            break

    return {
        "raw_query": raw,
        "normalized_query": normalized,
        "tokens": tokens,
        "vintage": vintage,
        "grape": grape,
        "country": country,
        "region": region,
        "subregion": subregion,
        "denomination": denomination,
    }
