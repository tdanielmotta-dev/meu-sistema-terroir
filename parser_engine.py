import re
from urllib.parse import urlparse

GRAPE_WORDS = [
    "Cabernet Sauvignon", "Cabernet Franc", "Merlot", "Malbec", "Syrah", "Shiraz",
    "Pinot Noir", "Chardonnay", "Sauvignon Blanc", "Riesling", "Nebbiolo",
    "Sangiovese", "Tempranillo", "Grenache", "Garnacha", "Carmenere", "Carménère",
    "Touriga Nacional", "Gewurztraminer", "Gewürztraminer", "Viognier", "Gamay"
]

COUNTRIES = [
    "França", "France", "Itália", "Italy", "Espanha", "Spain", "Portugal",
    "Chile", "Argentina", "Brasil", "Brazil", "USA", "United States",
    "South Africa", "África do Sul", "Germany", "Alemanha"
]

REGION_HINTS = [
    "Champagne", "Bordeaux", "Bourgogne", "Burgundy", "Piemonte", "Piedmont",
    "Toscana", "Tuscany", "Rioja", "Douro", "Mendoza", "Central Valley",
    "Chablis", "Barolo", "Barbaresco", "Sauternes", "Pomerol", "Margaux",
    "Napa Valley", "Langhe", "Uco Valley"
]

DENOM_HINTS = [
    "DOCG", "DOC", "DO", "DOP", "IGP", "AOC", "AOP", "AVA", "Champagne"
]

def blank_record():
    return {
        "producer": "",
        "wine_name": "",
        "vintage": "",
        "grape": "",
        "country": "",
        "region": "",
        "subregion": "",
        "denomination": "",
        "classification": "",
        "wine_type": "",
        "alcohol": "",
        "aromas": "",
        "palate": "",
        "acidity": "",
        "body": "",
        "soil": "",
        "climate": "",
        "terroir": "",
        "aging": "",
        "pairing": "",
        "notes": "",
    }

def normalize_text(text: str):
    return " ".join((text or "").split())

def extract_vintage(text: str):
    m = re.search(r"\b(19\d{2}|20\d{2}|21\d{2})\b", text or "")
    return m.group(1) if m else ""

def extract_alcohol(text: str):
    m = re.search(r"\b(\d{1,2}(?:[.,]\d)?)\s*%(\s*vol)?\b", text or "", flags=re.I)
    if m:
        return m.group(1).replace(",", ".") + "%"
    return ""

def extract_grape(text: str):
    txt = text or ""
    for g in sorted(GRAPE_WORDS, key=len, reverse=True):
        if g.lower() in txt.lower():
            return g
    return ""

def extract_region(text: str):
    txt = text or ""
    for r in sorted(REGION_HINTS, key=len, reverse=True):
        if r.lower() in txt.lower():
            return r
    return ""

def extract_country(text: str):
    txt = text or ""
    if re.search(r"\bChampagne\b", txt, flags=re.I):
        return "França"
    if re.search(r"\bBarolo\b|\bBarbaresco\b|\bPiemonte\b|\bPiedmont\b", txt, flags=re.I):
        return "Itália"
    if re.search(r"\bRioja\b", txt, flags=re.I):
        return "Espanha"
    if re.search(r"\bDouro\b", txt, flags=re.I):
        return "Portugal"

    for c in COUNTRIES:
        if c.lower() in txt.lower():
            mapping = {
                "France": "França",
                "Italy": "Itália",
                "Spain": "Espanha",
                "Brazil": "Brasil",
                "United States": "Estados Unidos",
                "South Africa": "África do Sul",
                "Germany": "Alemanha",
            }
            return mapping.get(c, c)
    return ""

def extract_denomination(text: str):
    txt = text or ""
    if re.search(r"\bChampagne\b", txt, flags=re.I):
        return "Champagne AOC"
    m = re.search(r"\b([A-Z][A-Za-zÀ-ÿ'’\- ]{1,40}\s(?:DOCG|DOC|DO|DOP|IGP|AOC|AOP|AVA))\b", txt)
    if m:
        return normalize_text(m.group(1))
    for d in DENOM_HINTS:
        if re.search(rf"\b{re.escape(d)}\b", txt, flags=re.I):
            return d
    return ""

def infer_type(text: str):
    txt = (text or "").lower()
    if "champagne" in txt or "sparkling" in txt or "espumante" in txt:
        return "Espumante"
    if "white wine" in txt or "vin blanc" in txt or "branco" in txt:
        return "Branco"
    if "rosé" in txt or "rose wine" in txt:
        return "Rosé"
    if "red wine" in txt or "tinto" in txt:
        return "Tinto"
    return ""

def domain_of(url: str):
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""

def parse_vivino_source(item: dict, query: str):
    title = item.get("title", "")
    snippet = item.get("snippet", "")
    text = normalize_text(title + " " + snippet)

    rec = blank_record()
    rec["vintage"] = extract_vintage(text)
    rec["grape"] = extract_grape(text)
    rec["country"] = extract_country(text)
    rec["region"] = extract_region(text)
    rec["denomination"] = extract_denomination(text)
    rec["wine_type"] = infer_type(text)

    # "X wine has 51 mentions of oaky notes"
    if "oaky" in text.lower():
        rec["aging"] = text

    # Heurística do nome
    raw = title.split(" - ")[0].strip()
    rec["wine_name"] = raw

    return rec

def parse_winesearcher_source(item: dict, query: str):
    title = item.get("title", "")
    snippet = item.get("snippet", "")
    text = normalize_text(title + " " + snippet)

    rec = blank_record()
    rec["vintage"] = extract_vintage(text)
    rec["grape"] = extract_grape(text)
    rec["country"] = extract_country(text)
    rec["region"] = extract_region(text)
    rec["denomination"] = extract_denomination(text)
    rec["wine_type"] = infer_type(text)
    rec["wine_name"] = title.split(" - ")[0].strip()

    return rec

def parse_official_or_generic_source(item: dict, query: str):
    title = item.get("title", "")
    snippet = item.get("snippet", "")
    text = normalize_text(title + " " + snippet)

    rec = blank_record()
    rec["vintage"] = extract_vintage(text)
    rec["alcohol"] = extract_alcohol(text)
    rec["grape"] = extract_grape(text)
    rec["country"] = extract_country(text)
    rec["region"] = extract_region(text)
    rec["denomination"] = extract_denomination(text)
    rec["wine_type"] = infer_type(text)

    # Heurísticas por marcas famosas
    q = (query or "").lower()
    if "dom perignon" in q or "dom pérignon" in q:
        rec["producer"] = "Moët & Chandon"
        rec["wine_name"] = "Dom Pérignon"
        if not rec["country"]:
            rec["country"] = "França"
        if not rec["region"]:
            rec["region"] = "Champagne"
        if not rec["denomination"]:
            rec["denomination"] = "Champagne AOC"
        if not rec["wine_type"]:
            rec["wine_type"] = "Espumante"
        if not rec["grape"]:
            rec["grape"] = "Chardonnay, Pinot Noir"
        rec["classification"] = "Prestige Cuvée"

    if not rec["wine_name"]:
        rec["wine_name"] = title.split(" - ")[0].strip()

    return rec

def parse_source_item(item: dict, query: str):
    url = item.get("url", "")
    domain = domain_of(url)

    if "vivino" in domain:
        parsed = parse_vivino_source(item, query)
        parser_name = "vivino"
    elif "wine-searcher" in domain:
        parsed = parse_winesearcher_source(item, query)
        parser_name = "wine_searcher"
    else:
        parsed = parse_official_or_generic_source(item, query)
        parser_name = "generic"

    parsed["_parser"] = parser_name
    parsed["_source_title"] = item.get("title", "")
    parsed["_source_url"] = item.get("url", "")
    parsed["_source_snippet"] = item.get("snippet", "")
    return parsed
