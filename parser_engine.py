import re

GRAPE_KEYWORDS = [
    "cabernet sauvignon", "cabernet franc", "merlot", "malbec", "pinot noir",
    "syrah", "shiraz", "nebbiolo", "sangiovese", "tempranillo", "chardonnay",
    "sauvignon blanc", "riesling", "pinot grigio", "pinot gris", "carmenere",
    "touriga nacional", "zinfandel", "grenache", "garnacha", "viognier",
    "gewurztraminer", "chenin blanc", "moscato", "glera", "corvina", "barbera"
]

COUNTRY_KEYWORDS = [
    "frança", "france", "itália", "italy", "espanha", "spain", "portugal",
    "chile", "argentina", "brasil", "austrália", "australia", "usa",
    "united states", "new zealand", "nova zelândia", "south africa"
]

REGION_KEYWORDS = [
    "bordeaux", "burgundy", "bourgogne", "champagne", "rioja", "dourot",
    "douro", "barolo", "barbaresco", "piemonte", "toscana", "chianti",
    "mendoza", "maipo", "colchagua", "casablanca", "central valley",
    "napa", "sonoma", "chablis", "côte de nuits", "cote de nuits"
]

DENOMINATION_KEYWORDS = [
    "docg", "doc", "aoc", "aop", "dop", "igp", "igt", "do", "ava", "wo"
]


def normalize_spaces(text: str) -> str:
    return " ".join((text or "").strip().split())


def extract_vintage(text: str):
    if not text:
        return None
    m = re.search(r"\b(19\d{2}|20\d{2}|21\d{2})\b", text)
    return m.group(1) if m else None


def find_keyword(text: str, candidates):
    t = (text or "").lower()
    best = None
    for c in sorted(candidates, key=len, reverse=True):
        if c.lower() in t:
            best = c
            break
    return best


def parse_wine_query(query: str):
    raw = query or ""
    normalized = normalize_spaces(raw)
    lowered = normalized.lower()

    vintage = extract_vintage(normalized)
    grape = find_keyword(lowered, GRAPE_KEYWORDS)
    country = find_keyword(lowered, COUNTRY_KEYWORDS)
    region = find_keyword(lowered, REGION_KEYWORDS)
    denomination = find_keyword(lowered, DENOMINATION_KEYWORDS)

    tokens = normalized.split()

    return {
        "raw_query": raw,
        "normalized_query": normalized,
        "tokens": tokens,
        "vintage": vintage,
        "grape": grape.title() if grape else None,
        "country": country.title() if country else None,
        "region": region.title() if region else None,
        "subregion": None,
        "denomination": denomination.upper() if denomination else None,
    }
