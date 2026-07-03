import re

GRAPES = [
    "Merlot", "Cabernet Sauvignon", "Cabernet Franc", "Pinot Noir",
    "Chardonnay", "Sauvignon Blanc", "Syrah", "Shiraz", "Malbec",
    "Nebbiolo", "Sangiovese", "Tempranillo", "Carmenere", "Carménère",
    "Tannat", "Grenache", "Garnacha", "Riesling", "Gewurztraminer",
    "Gewürztraminer", "Viognier", "Pinot Grigio", "Pinot Gris",
    "Zinfandel", "Primitivo", "Touriga Nacional", "Alvarinho", "Albariño"
]

COUNTRIES = [
    "França", "France", "Itália", "Italy", "Espanha", "Spain", "Portugal",
    "Argentina", "Chile", "Brasil", "Brazil", "Uruguai", "Uruguay",
    "Estados Unidos", "United States", "USA", "Austrália", "Australia",
    "Alemanha", "Germany", "África do Sul", "South Africa", "Nova Zelândia"
]

REGIONS = [
    "Bordeaux", "Bourgogne", "Burgundy", "Champagne", "Piemonte", "Toscana",
    "Rioja", "Douro", "Alentejo", "Mendoza", "Maipo", "Colchagua", "Napa",
    "Sonoma", "Mosel", "Alsace", "Loire", "Rhone", "Rhône", "Barolo",
    "Barbaresco", "Chablis", "Sauternes", "Médoc", "Margaux", "Pauillac"
]

CLASSIFICATIONS = [
    "DOCG", "DOC", "DOCa", "DOP", "IGP", "IGT", "AOC", "AOP", "DO"
]


def normalize_spaces(text: str) -> str:
    return " ".join((text or "").split()).strip()


def find_first(patterns, text, flags=re.I):
    for pat in patterns:
        m = re.search(pat, text, flags)
        if m:
            return normalize_spaces(m.group(1))
    return None


def extract_grapes(text: str):
    found = []
    lower = (text or "").lower()
    for grape in GRAPES:
        if grape.lower() in lower:
            found.append(grape)
    # remove duplicados preservando ordem
    out = []
    seen = set()
    for g in found:
        if g.lower() not in seen:
            seen.add(g.lower())
            out.append(g)
    return out


def extract_country(text: str):
    lower = (text or "").lower()
    for c in COUNTRIES:
        if c.lower() in lower:
            return c
    return None


def extract_region(text: str):
    lower = (text or "").lower()
    for r in REGIONS:
        if r.lower() in lower:
            return r
    return None


def extract_classification(text: str):
    for c in CLASSIFICATIONS:
        if re.search(rf"\b{re.escape(c)}\b", text or "", flags=re.I):
            return c
    return None


def extract_alcohol(text: str):
    if not text:
        return None

    patterns = [
        r'(\d{1,2}[.,]\d)\s*%\s*(?:vol|abv)?',
        r'(\d{1,2})\s*%\s*(?:vol|abv)?',
        r'alcool[^0-9]{0,20}(\d{1,2}[.,]\d)',
        r'alcohol[^0-9]{0,20}(\d{1,2}[.,]\d)',
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.I)
        if m:
            return m.group(1).replace(",", ".") + "%"

    return None


def extract_vintage(text: str):
    if not text:
        return None
    m = re.search(r"\b(19\d{2}|20\d{2}|21\d{2})\b", text)
    if m:
        return m.group(1)
    return None


def extract_denomination(text: str):
    if not text:
        return None

    patterns = [
        r'((?:[A-Z][A-Za-zÀ-ÿ\'\-]+\s){0,5}(?:DOCG|DOC|DOCa|AOC|AOP|DOP|IGP|IGT|DO))',
        r'(appellation\s+[A-Za-zÀ-ÿ\s\'\-]{3,80})',
        r'(denominazione\s+[A-Za-zÀ-ÿ\s\'\-]{3,80})'
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.I)
        if m:
            return normalize_spaces(m.group(1))
    return None


def extract_wine_type(text: str):
    if not text:
        return None
    lower = text.lower()

    candidates = [
        ("Espumante", ["sparkling", "espumante", "brut", "champagne", "cava", "prosecco"]),
        ("Rosé", ["rosé", "rose"]),
        ("Branco", ["white wine", "vin blanc", "bianco", "branco"]),
        ("Tinto", ["red wine", "rosso", "rouge", "tinto"]),
        ("Sobremesa / Doce", ["dessert wine", "late harvest", "sauternes", "botrytis", "sweet wine"])
    ]

    for label, keys in candidates:
        for k in keys:
            if k in lower:
                return label
    return None


def extract_simple_field(text: str, keywords):
    if not text:
        return None

    # pega sentença que contenha uma palavra-chave
    sentences = re.split(r'(?<=[\.\!\?])\s+', text)
    for sent in sentences:
        low = sent.lower()
        for kw in keywords:
            if kw.lower() in low and len(sent.strip()) >= 10:
                return normalize_spaces(sent.strip())
    return None


def extract_profile_from_text(query: str, title: str, snippet: str, page_summary: str):
    full = " ".join([
        query or "",
        title or "",
        snippet or "",
        page_summary or ""
    ]).strip()

    if not full:
        return {}

    grapes = extract_grapes(full)

    profile = {
        "producer": None,
        "wine_name": None,
        "vintage": extract_vintage(full),
        "grape": grapes[0] if grapes else None,
        "other_grapes": grapes[1:] if len(grapes) > 1 else [],
        "country": extract_country(full),
        "region": extract_region(full),
        "subregion": None,
        "denomination": extract_denomination(full),
        "classification": extract_classification(full),
        "wine_type": extract_wine_type(full),
        "alcohol": extract_alcohol(full),
        "climate": extract_simple_field(full, ["climate", "clima", "maritime", "continental", "atlantic"]),
        "soil": extract_simple_field(full, ["soil", "solo", "limestone", "chalk", "clay", "gravel", "slate", "argila", "calcário"]),
        "terroir": extract_simple_field(full, ["terroir", "vineyard", "vinhedo", "encostas", "parcel", "parcelas"]),
        "acidity": extract_simple_field(full, ["acidity", "acid", "acidez", "freshness", "fresco"]),
        "body": extract_simple_field(full, ["body", "encorpado", "médio corpo", "full-bodied", "medium-bodied"]),
        "tannins": extract_simple_field(full, ["tannin", "tanino", "taninos"]),
        "aging": extract_simple_field(full, ["oak", "barrel", "barrique", "barrica", "aged", "maturation", "aging", "envelhecimento"]),
        "aromas": extract_simple_field(full, ["aroma", "nose", "bouquet", "frutas", "floral", "especiarias"]),
        "palate": extract_simple_field(full, ["palate", "paladar", "taste", "sabor", "finish", "final"]),
        "pairing": extract_simple_field(full, ["pairing", "harmoniza", "food pairing", "serve with"]),
        "notes": normalize_spaces(snippet or page_summary or "")
    }

    # tentativa de nome do vinho / produtor baseada no título
    title_clean = normalize_spaces(title or "")
    if title_clean:
        profile["wine_name"] = title_clean[:180]

    # tentativa de produtor: se título tiver separador comum
    producer = guess_producer_from_title(title_clean)
    if producer:
        profile["producer"] = producer

    return {k: v for k, v in profile.items() if v not in [None, "", [], {}]}


def guess_producer_from_title(title: str):
    if not title:
        return None

    separators = [" - ", " | ", " – ", " — "]
    for sep in separators:
        if sep in title:
            left = title.split(sep)[0].strip()
            if 2 <= len(left) <= 80:
                return left

    return None
