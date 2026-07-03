import re


KNOWN_DENOMINATIONS = [
    "Barolo DOCG",
    "Barbaresco DOCG",
    "Rioja DOCa",
    "Bordeaux AOC",
    "Sauternes AOC",
    "Margaux AOC",
    "Pauillac AOC",
    "Chianti Classico DOCG",
]

KNOWN_REGIONS = [
    "Bordeaux",
    "Piemonte",
    "Rioja",
    "Toscana",
    "Douro",
    "Champagne",
    "Bourgogne",
    "Barolo",
    "Sauternes",
]

KNOWN_COUNTRIES = [
    "França",
    "Itália",
    "Espanha",
    "Portugal",
    "Argentina",
    "Chile",
    "Brasil",
    "Alemanha",
    "Estados Unidos",
]


def extract_vintage(text: str):
    if not text:
        return None
    match = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    return match.group(1) if match else None


def detect_known_term(text: str, options: list[str]):
    if not text:
        return None
    text_lower = text.lower()
    for item in options:
        if item.lower() in text_lower:
            return item
    return None


def parse_query(query: str):
    query = (query or "").strip()

    parsed = {
        "raw_query": query,
        "vintage": extract_vintage(query),
        "denomination_hint": detect_known_term(query, KNOWN_DENOMINATIONS),
        "region_hint": detect_known_term(query, KNOWN_REGIONS),
        "country_hint": detect_known_term(query, KNOWN_COUNTRIES),
    }

    return parsed
