import re

KNOWN_GRAPES = [
    "cabernet sauvignon", "cabernet franc", "merlot", "pinot noir",
    "chardonnay", "sauvignon blanc", "riesling", "syrah", "shiraz",
    "malbec", "nebbiolo", "sangiovese", "tempranillo", "grenache",
    "garnacha", "mourvedre", "monastrell", "carignan", "carmenere",
    "carménère", "touriga nacional", "chenin blanc", "gewurztraminer",
    "viognier", "albarino", "albariño", "semillon", "sémillon",
    "petit verdot", "zinfandel", "barbera", "dolcetto"
]

KNOWN_COUNTRIES = [
    "frança", "france", "itália", "italia", "espanha", "spain",
    "portugal", "argentina", "chile", "brasil", "alemanha",
    "germany", "austrália", "australia", "eua", "usa",
    "estados unidos", "nova zelândia", "new zealand",
    "áfrica do sul", "south africa"
]

KNOWN_REGIONS = [
    "bordeaux", "bourgogne", "burgundy", "champagne", "alsace",
    "loire", "rhône", "rhone", "barolo", "barbaresco", "piemonte",
    "piedmont", "toscana", "tuscany", "chianti", "montalcino",
    "rioja", "ribera del duero", "priorat", "douro", "dão", "dao",
    "vinho verde", "mendoza", "maipo", "colchagua", "mosel",
    "rheingau", "napa valley", "sonoma", "barossa", "marlborough",
    "stellenbosch", "valle central", "maipo valley", "colchagua valley"
]

KNOWN_DENOMINATIONS = [
    "aoc", "aop", "doc", "docg", "igp", "dop", "igt", "doca",
    "bordeaux aoc", "barolo docg", "barbaresco docg",
    "chianti classico docg", "rioja doca", "douro doc"
]


def normalize_text(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_vintage(text: str):
    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    return years[0] if years else None


def find_first_match(text: str, candidates: list):
    text_lower = text.lower()
    for item in candidates:
        if item.lower() in text_lower:
            return item
    return None


def tokenize_query(text: str):
    return re.findall(r"[a-zA-ZÀ-ÿ0-9\-']+", text.lower())


def parse_wine_query(query: str):
    normalized = normalize_text(query)
    return {
        "original_query": query,
        "normalized_query": normalized,
        "vintage": extract_vintage(normalized),
        "grape": find_first_match(normalized, KNOWN_GRAPES),
        "country": find_first_match(normalized, KNOWN_COUNTRIES),
        "region": find_first_match(normalized, KNOWN_REGIONS),
        "denomination": find_first_match(normalized, KNOWN_DENOMINATIONS),
        "tokens": tokenize_query(normalized)
    }
