import re

KNOWN_GRAPES = [
    "cabernet sauvignon", "cabernet franc", "merlot", "malbec", "pinot noir",
    "syrah", "shiraz", "nebbiolo", "tempranillo", "chardonnay", "sauvignon blanc",
    "riesling", "gewurztraminer", "carmenere", "sangiovese"
]

KNOWN_COUNTRIES = [
    "frança", "italia", "itália", "espanha", "portugal", "argentina", "chile",
    "brasil", "uruguai", "estados unidos", "australia", "austrália", "alemanha"
]

KNOWN_DENOMINATIONS = [
    "docg", "doc", "aoc", "dop", "igp", "do", "ava", "igt", "premier cru", "grand cru"
]


def parse_wine_query(query: str):
    raw = (query or "").strip()
    normalized = " ".join(raw.split())
    lower = normalized.lower()

    vintage = None
    m = re.search(r"\b(19\d{2}|20\d{2})\b", lower)
    if m:
        vintage = m.group(1)

    grape = None
    for g in sorted(KNOWN_GRAPES, key=len, reverse=True):
        if g in lower:
            grape = g.title()
            break

    denomination = None
    for d in sorted(KNOWN_DENOMINATIONS, key=len, reverse=True):
        if d in lower:
            denomination = d.upper() if len(d) <= 4 else d.title()
            break

    country = None
    for c in KNOWN_COUNTRIES:
        if c in lower:
            country = c.title()
            break

    tokens = normalized.split()

    return {
        "raw_query": raw,
        "normalized_query": normalized,
        "tokens": tokens,
        "vintage": vintage,
        "grape": grape,
        "country": country,
        "region": None,
        "subregion": None,
        "denomination": denomination
    }
