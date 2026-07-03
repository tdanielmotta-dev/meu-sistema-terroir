import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
}

FIELD_PATTERNS = {
    "alcohol": [
        r"(\d{1,2}[.,]\d)\s*%",
        r"(\d{1,2})\s*%"
    ],
    "vintage": [
        r"\b(19\d{2}|20\d{2})\b"
    ]
}

GRAPES = [
    "Cabernet Sauvignon", "Cabernet Franc", "Merlot", "Malbec", "Pinot Noir",
    "Syrah", "Shiraz", "Nebbiolo", "Tempranillo", "Chardonnay", "Sauvignon Blanc",
    "Riesling", "Gewurztraminer", "Carmenere", "Sangiovese"
]

COUNTRIES = [
    "France", "França", "Italy", "Itália", "Italia", "Spain", "Espanha", "Portugal",
    "Argentina", "Chile", "Brazil", "Brasil", "Uruguay", "Uruguai", "USA", "Estados Unidos"
]

REGIONS = [
    "Bordeaux", "Bourgogne", "Burgundy", "Chablis", "Champagne", "Piemonte",
    "Barolo", "Barbaresco", "Toscana", "Rioja", "Douro", "Mendoza",
    "Central Valley", "Maipo", "Colchagua", "Casablanca"
]

DENOMS = [
    "DOCG", "DOC", "AOC", "DOP", "IGP", "DO", "AVA", "IGT",
    "Barolo DOCG", "Bordeaux AOC", "Chablis Premier Cru"
]


def safe_get_text(url: str):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=25)
        resp.raise_for_status()
        html = resp.text
        soup = BeautifulSoup(html, "lxml")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            meta_desc = meta["content"].strip()

        paragraphs = []
        for p in soup.find_all("p"):
            txt = p.get_text(" ", strip=True)
            if len(txt) >= 40:
                paragraphs.append(txt)
            if len(paragraphs) >= 25:
                break

        full_text = "\n".join([title, meta_desc] + paragraphs)
        return full_text[:40000]
    except Exception:
        return ""


def first_match(patterns, text):
    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            return m.group(1)
    return ""


def find_keyword_from_list(text, values):
    low = text.lower()
    for item in sorted(values, key=len, reverse=True):
        if item.lower() in low:
            return item
    return ""


def extract_sentence_with_keywords(text, keywords, max_len=300):
    chunks = re.split(r"(?<=[\.\!\?])\s+", text)
    low_keywords = [k.lower() for k in keywords]

    for ch in chunks:
        cl = ch.lower()
        if any(k in cl for k in low_keywords):
            return ch[:max_len]
    return ""


def parse_source(url: str, title: str = "", snippet: str = ""):
    text = safe_get_text(url)
    combined = " ".join([title or "", snippet or "", text or ""]).strip()

    if not combined:
        return {
            "source_url": url,
            "source_title": title,
            "source_snippet": snippet,
            "extracted": {}
        }

    alcohol = first_match(FIELD_PATTERNS["alcohol"], combined)
    vintage = first_match(FIELD_PATTERNS["vintage"], combined)
    grape = find_keyword_from_list(combined, GRAPES)
    country = find_keyword_from_list(combined, COUNTRIES)
    region = find_keyword_from_list(combined, REGIONS)
    denomination = find_keyword_from_list(combined, DENOMS)

    aromas = extract_sentence_with_keywords(
        combined,
        ["aroma", "aromas", "nose", "bouquet", "frutas", "plum", "cherry", "violet"]
    )
    palate = extract_sentence_with_keywords(
        combined,
        ["palate", "paladar", "boca", "taninos", "finish", "final", "body", "corpo"]
    )
    acidity = extract_sentence_with_keywords(
        combined,
        ["acidity", "acidez", "fresh", "fresco"]
    )
    soil = extract_sentence_with_keywords(
        combined,
        ["soil", "solo", "chalk", "clay", "limestone", "gravel", "argila", "calcário", "marga"]
    )
    climate = extract_sentence_with_keywords(
        combined,
        ["climate", "clima", "continental", "maritime", "mediterranean", "oceânico"]
    )
    terroir = extract_sentence_with_keywords(
        combined,
        ["terroir", "vineyard", "vinhedo", "altitude", "encosta", "parcel"]
    )
    aging = extract_sentence_with_keywords(
        combined,
        ["oak", "barrel", "barrica", "aging", "aged", "maturation", "carvalho"]
    )
    pairing = extract_sentence_with_keywords(
        combined,
        ["pairing", "harmonization", "harmonização", "serve with", "food pairing"]
    )

    extracted = {
        "alcohol": alcohol,
        "vintage": vintage,
        "grape": grape,
        "country": country,
        "region": region,
        "denomination": denomination,
        "aromas": aromas,
        "palate": palate,
        "acidity": acidity,
        "soil": soil,
        "climate": climate,
        "terroir": terroir,
        "aging": aging,
        "pairing": pairing,
        "raw_excerpt": combined[:2500]
    }

    return {
        "source_url": url,
        "source_title": title,
        "source_snippet": snippet,
        "extracted": extracted
    }
