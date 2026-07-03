import re


KNOWN_GRAPES = [
    "cabernet sauvignon",
    "cabernet franc",
    "merlot",
    "pinot noir",
    "chardonnay",
    "sauvignon blanc",
    "riesling",
    "syrah",
    "shiraz",
    "malbec",
    "nebbiolo",
    "sangiovese",
    "tempranillo",
    "grenache",
    "garnacha",
    "mourvedre",
    "monastrell",
    "carignan",
    "carmenere",
    "touriga nacional",
    "chenin blanc",
    "gewurztraminer",
    "viognier",
    "albarino",
    "albariño",
    "semillon",
    "sémillon",
    "petit verdot",
    "zinfandel",
    "barbera",
    "dolcetto"
]

KNOWN_COUNTRIES = [
    "frança", "france", "itália", "italia", "espanha", "spain", "portugal",
    "argentina", "chile", "brasil", "alemanha", "germany", "austrália",
    "australia", "eua", "usa", "estados unidos", "nova zelândia",
    "new zealand", "áfrica do sul", "south africa"
]

KNOWN_REGIONS = [
    "bordeaux", "medoc", "médoc", "pauillac", "margaux", "saint-estephe",
    "saint-estèphe", "saint-julien", "pomerol", "saint-emilion",
    "saint-émilion", "sauternes", "barsac", "graves", "bourgogne",
    "burgundy", "chablis", "côte de nuits", "cote de nuits",
    "côte de beaune", "cote de beaune", "champagne", "alsace", "loire",
    "rhône", "rhone", "barolo", "barbaresco", "piemonte", "piedmont",
    "toscana", "tuscany", "chianti", "montalcino", "montepulciano",
    "rioja", "rioja alta", "rioja alavesa", "ribera del duero", "priorat",
    "rueda", "jerez", "douro", "dão", "dao", "vinho verde", "alentejo",
    "mendoza", "maipo", "colchagua", "vale do casablanca", "mosel",
    "rheingau", "napa valley", "sonoma", "mclaren vale", "barossa",
    "marlborough", "stellenbosch", "mantiqueira"
]

KNOWN_DENOMINATIONS = [
    "aoc", "aop", "doc", "docg", "igp", "dop", "igt", "vin de france",
    "bordeaux aoc", "pauillac aoc", "margaux aoc", "saint-emilion grand cru",
    "barolo docg", "barbaresco docg", "chianti classico docg",
    "brunello di montalcino docg", "rioja doca", "ribera del duero do",
    "douro doc", "vinho verde doc"
]


def normalize_text(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_vintage(text: str):
    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    if years:
        return years[0]
    return None


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
    vintage = extract_vintage(normalized)
    grape = find_first_match(normalized, KNOWN_GRAPES)
    country = find_first_match(normalized, KNOWN_COUNTRIES)
    region = find_first_match(normalized, KNOWN_REGIONS)
    denomination = find_first_match(normalized, KNOWN_DENOMINATIONS)
    tokens = tokenize_query(normalized)

    return {
        "original_query": query,
        "normalized_query": normalized,
        "vintage": vintage,
        "grape": grape,
        "country": country,
        "region": region,
        "denomination": denomination,
        "tokens": tokens
    }
