import re

KNOWN_GRAPES = [
    "Merlot", "Cabernet Sauvignon", "Cabernet Franc", "Pinot Noir",
    "Chardonnay", "Sauvignon Blanc", "Syrah", "Shiraz", "Malbec",
    "Nebbiolo", "Sangiovese", "Tempranillo", "Carmenere", "Carménère",
    "Tannat", "Grenache", "Garnacha", "Riesling", "Gewurztraminer",
    "Gewürztraminer", "Viognier", "Pinot Grigio", "Pinot Gris",
    "Zinfandel", "Primitivo", "Touriga Nacional", "Alvarinho", "Albariño"
]

KNOWN_DENOM_TERMS = [
    "DOCG", "DOC", "DOP", "IGP", "IGT", "AOC", "AOP", "DO", "DOCa"
]

STYLE_TERMS = [
    "Reserva", "Gran Reserva", "Classico", "Clásico", "Classic",
    "Rosé", "Rose", "Brut", "Extra Brut", "Demi-Sec", "Sec", "Dry",
    "Late Harvest", "Botrytis", "Icewine"
]


def parse_wine_query(query: str) -> dict:
    query = (query or "").strip()
    if not query:
        return {
            "raw_query": "",
            "normalized_query": "",
            "vintage": None,
            "grapes_found": [],
            "denom_terms_found": [],
            "style_terms_found": [],
            "tokens": [],
            "producer_guess": None,
            "wine_name_guess": None
        }

    cleaned = " ".join(query.split())
    tokens = cleaned.split()

    vintage = None
    m = re.search(r"\b(19\d{2}|20\d{2}|21\d{2})\b", cleaned)
    if m:
        vintage = m.group(1)

    grapes_found = []
    lower_q = cleaned.lower()
    for grape in KNOWN_GRAPES:
        if grape.lower() in lower_q:
            grapes_found.append(grape)

    denom_terms_found = []
    for term in KNOWN_DENOM_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", cleaned, flags=re.I):
            denom_terms_found.append(term)

    style_terms_found = []
    for term in STYLE_TERMS:
        if term.lower() in lower_q:
            style_terms_found.append(term)

    producer_guess = None
    wine_name_guess = None

    # tentativa simples:
    # se tiver safra, tudo antes dela vira base do nome
    base = cleaned
    if vintage:
        base = cleaned.replace(vintage, "").strip()

    # remove duplicações de espaço
    base = " ".join(base.split())

    # se tiver uva conhecida, tenta dividir produtor e nome
    # ex: Gato Negro Merlot -> produtor=Gato Negro / wine=Merlot
    producer_guess = base
    wine_name_guess = base

    if grapes_found:
        grape = grapes_found[0]
        idx = base.lower().find(grape.lower())
        if idx > 0:
            left = base[:idx].strip()
            right = base[idx:].strip()
            if left:
                producer_guess = left
            wine_name_guess = right
        else:
            wine_name_guess = grape

    # fallback: se tiver 2+ palavras, assume primeira metade como produtor aproximado
    if not grapes_found and len(tokens) >= 2:
        producer_guess = " ".join(tokens[:-1]).replace(vintage or "", "").strip()
        wine_name_guess = cleaned.replace(producer_guess, "", 1).replace(vintage or "", "").strip()
        if not wine_name_guess:
            wine_name_guess = cleaned

    return {
        "raw_query": query,
        "normalized_query": cleaned,
        "vintage": vintage,
        "grapes_found": grapes_found,
        "denom_terms_found": denom_terms_found,
        "style_terms_found": style_terms_found,
        "tokens": tokens,
        "producer_guess": producer_guess,
        "wine_name_guess": wine_name_guess
    }
