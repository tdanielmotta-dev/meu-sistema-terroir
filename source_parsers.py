import re


GRAPES = [
    "Cabernet Sauvignon", "Cabernet Franc", "Merlot", "Malbec", "Pinot Noir",
    "Syrah", "Shiraz", "Nebbiolo", "Sangiovese", "Tempranillo", "Chardonnay",
    "Sauvignon Blanc", "Riesling", "Pinot Grigio", "Pinot Gris", "Carmenere",
    "Touriga Nacional", "Zinfandel", "Grenache", "Garnacha", "Viognier",
    "Gewurztraminer", "Chenin Blanc", "Moscato", "Glera", "Corvina", "Barbera"
]

COUNTRIES = [
    "France", "França", "Italy", "Itália", "Spain", "Espanha", "Portugal",
    "Chile", "Argentina", "Brazil", "Brasil", "Australia", "USA", "South Africa"
]

REGIONS = [
    "Champagne", "Bordeaux", "Bourgogne", "Burgundy", "Rioja", "Douro",
    "Piemonte", "Toscana", "Mendoza", "Maipo", "Colchagua", "Casablanca",
    "Central Valley", "Napa", "Sonoma", "Barolo", "Barbaresco", "Chablis"
]

DENOMS = ["DOCG", "DOC", "AOC", "AOP", "DOP", "IGP", "IGT", "DO", "AVA", "WO"]


def _find_first(text, options):
    txt = (text or "").lower()
    for op in sorted(options, key=len, reverse=True):
        if op.lower() in txt:
            return op
    return ""


def _extract_vintage(text):
    if not text:
        return ""
    m = re.search(r"\b(19\d{2}|20\d{2}|21\d{2})\b", text)
    return m.group(1) if m else ""


def _extract_alcohol(text):
    if not text:
        return ""
    patterns = [
        r"(\d{1,2}(?:[\.,]\d)?)\s*%",
        r"(\d{1,2}(?:[\.,]\d)?)\s*%?\s*vol",
        r"alcohol[:\s]+(\d{1,2}(?:[\.,]\d)?)"
    ]
    for p in patterns:
        m = re.search(p, text, flags=re.I)
        if m:
            return m.group(1).replace(",", ".") + "%"
    return ""


def _extract_simple_field(text, keywords):
    low = (text or "").lower()
    hits = [k for k in keywords if k.lower() in low]
    return ", ".join(hits[:3]) if hits else ""


def parse_source_result(source: dict):
    title = source.get("title", "") or ""
    snippet = source.get("snippet", "") or ""
    page_text = source.get("page_text", "") or ""

    blob = " ".join([title, snippet, page_text])

    out = {
        "producer": "",
        "wine_name": "",
        "vintage": _extract_vintage(blob),
        "grape": _extract_simple_field(blob, GRAPES),
        "country": _find_first(blob, COUNTRIES),
        "region": _find_first(blob, REGIONS),
        "subregion": "",
        "denomination": _find_first(blob, DENOMS),
        "classification": "",
        "wine_type": "",
        "alcohol": _extract_alcohol(blob),
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
        "raw_excerpt": blob[:3000]
    }

    low = blob.lower()

    # tipo
    if "sparkling wine" in low or "champagne" in low or "espumante" in low:
        out["wine_type"] = "Espumante"
    elif "white wine" in low or "vinho branco" in low:
        out["wine_type"] = "Branco"
    elif "rosé" in low or "rose wine" in low or "vinho rosé" in low:
        out["wine_type"] = "Rosé"
    elif "red wine" in low or "vinho tinto" in low:
        out["wine_type"] = "Tinto"

    # aromas / palate / acidity / body / aging
    aroma_keys = ["cherry", "blackberry", "plum", "citrus", "apple", "brioche", "vanilla", "oak", "floral", "mineral"]
    palate_keys = ["smooth", "creamy", "fresh", "fruity", "dry", "balanced", "structured", "elegant", "long finish"]
    acidity_keys = ["high acidity", "medium acidity", "bright acidity", "fresh acidity"]
    body_keys = ["light-bodied", "medium-bodied", "full-bodied", "medium body", "full body"]

    found_aromas = [k for k in aroma_keys if k in low]
    found_palate = [k for k in palate_keys if k in low]
    found_acidity = [k for k in acidity_keys if k in low]
    found_body = [k for k in body_keys if k in low]

    if found_aromas:
        out["aromas"] = ", ".join(found_aromas[:8])
    if found_palate:
        out["palate"] = ", ".join(found_palate[:8])
    if found_acidity:
        out["acidity"] = ", ".join(found_acidity[:4])
    if found_body:
        out["body"] = ", ".join(found_body[:4])

    if "oak" in low or "oaky" in low or "barrel" in low or "aged" in low:
        out["aging"] = "Há indícios de amadurecimento / notas de carvalho na fonte."

    # heurística simples para produtor/nome do vinho a partir do título
    cleaned_title = title.replace("–", "-").replace("|", "-")
    parts = [p.strip() for p in cleaned_title.split("-") if p.strip()]
    if parts:
        main = parts[0]
        out["notes"] = f"Extraído de fonte online: {title}"

        # tenta quebrar produtor + vinho
        words = main.split()
        if len(words) >= 2:
            out["producer"] = " ".join(words[:2])
            out["wine_name"] = " ".join(words[2:]) if len(words) > 2 else main

    return out
