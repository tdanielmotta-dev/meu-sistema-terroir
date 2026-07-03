import re
from typing import Dict, List, Optional


YEAR_PATTERN = re.compile(r"\b(19\d{2}|20\d{2}|2100)\b", re.IGNORECASE)

CLASSIFICATION_PATTERNS = [
    "DOCG", "DOC", "DOCa", "DOP", "IGP", "IGT",
    "AOC", "AOP", "DO", "D.O.", "AVA",
    "QmP", "Prädikatswein", "VDP", "Grand Cru", "Premier Cru"
]

QUALITY_TERMS = [
    "Reserva", "Gran Reserva", "Riserva", "Classico", "Superiore",
    "Grand Cru", "Premier Cru", "Estate", "Single Vineyard",
    "Vieilles Vignes", "LBV", "Vintage", "Colheita", "Reserva Especial"
]

STYLE_KEYWORDS = {
    "tinto": ["rosso", "red", "tinto", "rouge"],
    "branco": ["bianco", "white", "branco", "blanc"],
    "rose": ["rosé", "rose", "rosato"],
    "espumante": ["brut", "extra brut", "nature", "cava", "champagne", "espumante", "spumante", "prosecco"],
    "fortificado": ["porto", "port", "sherry", "jerez", "madeira", "marsala", "lbv", "vintage port"],
    "doce": ["sauternes", "tokaji", "late harvest", "icewine", "vendange tardive", "passito", "beerenauslese", "trockenbeerenauslese"]
}

GRAPE_HINTS = [
    "Merlot", "Cabernet Sauvignon", "Cabernet Franc", "Petit Verdot", "Malbec", "Carmenère",
    "Pinot Noir", "Chardonnay", "Sauvignon Blanc", "Semillon", "Sémillon",
    "Syrah", "Shiraz", "Nebbiolo", "Sangiovese", "Tempranillo",
    "Malbec", "Carménère", "Riesling", "Gewurztraminer", "Gewürztraminer",
    "Touriga Nacional", "Tannat", "Zinfandel", "Grenache", "Garnacha",
    "Barbera", "Dolcetto", "Mencía", "Alvarinho", "Arinto", "Baga",
    "Encruzado", "Viognier", "Mourvèdre", "Pinot Meunier"
]

COUNTRY_HINTS = {
    "França": [
        "frança", "france", "bordeaux", "bourgogne", "burgundy", "champagne",
        "alsace", "loire", "rhône", "rhone", "médoc", "medoc", "pauillac",
        "margaux", "saint-émilion", "saint emilion", "sauternes", "chablis",
        "pommerol", "pomerol", "graves"
    ],
    "Itália": [
        "italia", "itália", "piemonte", "barolo", "barbaresco", "chianti",
        "brunello", "toscana", "amarone", "valpolicella", "soave", "prosecco",
        "montalcino", "montepulciano"
    ],
    "Espanha": [
        "espanha", "spain", "rioja", "ribera del duero", "priorat", "jerez",
        "cava", "rueda", "rias baixas", "bierzo", "ribeiro", "rías baixas"
    ],
    "Portugal": [
        "portugal", "douro", "dao", "dão", "vinho verde", "alentejo", "porto",
        "madeira", "bairrada", "colares", "setúbal", "setubal"
    ],
    "Argentina": [
        "argentina", "mendoza", "salta", "patagonia", "patagônia", "malbec"
    ],
    "Chile": [
        "chile", "maipo", "colchagua", "casablanca", "aconcagua", "carmenere", "carménère"
    ],
    "Brasil": [
        "brasil", "vale dos vinhedos", "serra gaúcha", "serra gaucha",
        "campanha gaúcha", "campanha gaucha", "mantiqueira", "altos de pinto bandeira"
    ],
    "Alemanha": [
        "germany", "deutschland", "alemã", "alemanha", "mosel", "rheingau",
        "pfalz", "baden", "nahe", "riesling"
    ],
    "EUA": [
        "usa", "u.s.a.", "united states", "california", "napa", "sonoma",
        "oregon", "washington", "willamette"
    ],
    "Austrália": [
        "australia", "austrália", "barossa", "mclaren vale", "yarra valley",
        "margaret river", "hunter valley"
    ]
}

REGION_HINTS = [
    "Bordeaux", "Médoc", "Margaux", "Pauillac", "Saint-Émilion", "Saint-Emilion", "Pomerol",
    "Sauternes", "Barsac", "Graves", "Bourgogne", "Chablis", "Champagne", "Alsace",
    "Barolo", "Barbaresco", "Piemonte", "Chianti", "Chianti Classico",
    "Brunello di Montalcino", "Toscana", "Valpolicella", "Amarone",
    "Rioja", "Ribera del Duero", "Priorat", "Rías Baixas", "Jerez",
    "Douro", "Dão", "Vinho Verde", "Alentejo", "Bairrada", "Porto", "Madeira",
    "Vale dos Vinhedos", "Campanha Gaúcha", "Mantiqueira", "Pinto Bandeira",
    "Napa Valley", "Sonoma", "Willamette Valley", "Mosel", "Rheingau"
]

PRODUCER_PREFIXES = [
    "Château", "Chateau", "Domaine", "Dom.", "Bodega", "Cantina", "Tenuta",
    "Quinta", "Adega", "Casa", "Clos", "Weingut", "Marchesi", "Famiglia"
]


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def find_year(text: str) -> Optional[str]:
    m = YEAR_PATTERN.search(text or "")
    return m.group(1) if m else None


def extract_terms(text: str, candidates: List[str]) -> List[str]:
    text_low = (text or "").lower()
    found = []
    for item in candidates:
        if item.lower() in text_low:
            found.append(item)
    return found


def infer_country(text: str):
    text_low = (text or "").lower()
    scores = {}
    for country, hints in COUNTRY_HINTS.items():
        score = 0
        for hint in hints:
            if hint.lower() in text_low:
                score += 1
        if score > 0:
            scores[country] = score

    if not scores:
        return None, 0.0

    best = sorted(scores.items(), key=lambda x: x[1], reverse=True)[0]
    # score simples normalizado
    conf = min(1.0, 0.35 + (best[1] * 0.15))
    return best[0], round(conf, 4)


def infer_style(text: str):
    text_low = (text or "").lower()
    found = []
    scores = {}
    for style, terms in STYLE_KEYWORDS.items():
        hit = 0
        for t in terms:
            if t.lower() in text_low:
                hit += 1
        if hit > 0:
            found.append(style)
            scores[style] = round(min(1.0, 0.35 + hit * 0.18), 4)
    return found, scores


def extract_regions(text: str):
    found = extract_terms(text, REGION_HINTS)
    score = round(min(1.0, 0.30 + 0.12 * len(found)), 4) if found else 0.0
    return found, score


def extract_classifications(text: str):
    found = extract_terms(text, CLASSIFICATION_PATTERNS)
    score = round(min(1.0, 0.40 + 0.18 * len(found)), 4) if found else 0.0
    return found, score


def extract_quality_terms(text: str):
    found = extract_terms(text, QUALITY_TERMS)
    score = round(min(1.0, 0.30 + 0.12 * len(found)), 4) if found else 0.0
    return found, score


def extract_grapes(text: str):
    found = extract_terms(text, GRAPE_HINTS)
    score = round(min(1.0, 0.35 + 0.12 * len(found)), 4) if found else 0.0
    return found, score


def clean_for_label(text: str, year: Optional[str], classifications: List[str], quality_terms: List[str], regions: List[str]):
    clean = normalize_spaces(text)

    if year:
        clean = re.sub(rf"\b{re.escape(year)}\b", " ", clean, flags=re.IGNORECASE)

    for token in classifications + quality_terms + regions:
        clean = re.sub(rf"\b{re.escape(token)}\b", " ", clean, flags=re.IGNORECASE)

    clean = normalize_spaces(clean)
    return clean


def guess_producer_and_wine_name(text: str, year=None, classifications=None, quality_terms=None, regions=None):
    classifications = classifications or []
    quality_terms = quality_terms or []
    regions = regions or []

    clean = clean_for_label(text, year, classifications, quality_terms, regions)
    parts = clean.split()

    if not parts:
        return {
            "producer_guess": None,
            "wine_name_guess": None,
            "producer_confidence": 0.0,
            "wine_name_confidence": 0.0
        }

    # regra 1: prefixo típico de produtor
    if len(parts) >= 2 and parts[0] in PRODUCER_PREFIXES:
        producer = " ".join(parts[:2]) if len(parts) >= 2 else parts[0]
        wine_name = " ".join(parts[2:]) if len(parts) > 2 else None
        return {
            "producer_guess": producer,
            "wine_name_guess": wine_name,
            "producer_confidence": 0.88,
            "wine_name_confidence": 0.62 if wine_name else 0.0
        }

    # regra 2: até 2 palavras -> pode ser produtor só
    if len(parts) == 1:
        return {
            "producer_guess": None,
            "wine_name_guess": parts[0],
            "producer_confidence": 0.0,
            "wine_name_confidence": 0.45
        }

    if len(parts) == 2:
        return {
            "producer_guess": parts[0],
            "wine_name_guess": parts[1],
            "producer_confidence": 0.48,
            "wine_name_confidence": 0.45
        }

    # regra 3: 2 primeiras produtor / resto vinho
    producer = " ".join(parts[:2])
    wine_name = " ".join(parts[2:]) if len(parts) > 2 else None

    return {
        "producer_guess": producer,
        "wine_name_guess": wine_name,
        "producer_confidence": 0.58,
        "wine_name_confidence": 0.52 if wine_name else 0.0
    }


def parse_wine_query(text: str) -> Dict:
    text = normalize_spaces(text)

    year = find_year(text)
    year_conf = 1.0 if year else 0.0

    classifications, classification_conf = extract_classifications(text)
    quality_terms, quality_conf = extract_quality_terms(text)
    grapes, grapes_conf = extract_grapes(text)
    styles, style_scores = infer_style(text)
    style_conf = max(style_scores.values()) if style_scores else 0.0
    country, country_conf = infer_country(text)
    regions, region_conf = extract_regions(text)

    producer_block = guess_producer_and_wine_name(
        text,
        year=year,
        classifications=classifications,
        quality_terms=quality_terms,
        regions=regions
    )

    return {
        "raw_query": text,

        "producer_guess": producer_block["producer_guess"],
        "wine_name_guess": producer_block["wine_name_guess"],
        "year": year,
        "country_guess": country,
        "regions_detected": regions,
        "classifications": classifications,
        "quality_terms": quality_terms,
        "grapes_detected": grapes,
        "styles_detected": styles,

        "confidence": {
            "producer": producer_block["producer_confidence"],
            "wine_name": producer_block["wine_name_confidence"],
            "year": year_conf,
            "country": country_conf,
            "regions": region_conf,
            "classifications": classification_conf,
            "quality_terms": quality_conf,
            "grapes": grapes_conf,
            "styles": style_conf,
        },

        "style_scores": style_scores
    }
