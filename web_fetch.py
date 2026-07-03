import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WineIndex/1.0)"
}

# -----------------------------
# BUSCA / DOWNLOAD
# -----------------------------

def safe_get(url: str, timeout: int = 20):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception:
        return None


def duckduckgo_search(query: str, max_results: int = 6):
    query = (query or "").strip()
    if not query:
        return []

    search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    resp = safe_get(search_url)
    if not resp:
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    results = []

    for a in soup.select("a.result__a"):
        title = a.get_text(" ", strip=True)
        url = a.get("href", "").strip()

        snippet = ""
        wrapper = a.find_parent("div", class_="result")
        if wrapper:
            sn = wrapper.select_one(".result__snippet")
            if sn:
                snippet = sn.get_text(" ", strip=True)

        if title and url:
            results.append({
                "title": title,
                "url": url,
                "snippet": snippet
            })

        if len(results) >= max_results:
            break

    return results


def extract_page_text(url: str):
    resp = safe_get(url, timeout=20)
    if not resp:
        return ""

    soup = BeautifulSoup(resp.text, "lxml")

    for tag in soup(["script", "style", "noscript", "header", "footer"]):
        tag.decompose()

    chunks = []

    # meta description
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        chunks.append(meta.get("content", "").strip())

    # headings
    for tag in soup.find_all(["h1", "h2", "h3"]):
        txt = tag.get_text(" ", strip=True)
        if txt and len(txt) >= 3:
            chunks.append(txt)

    # paragraphs / list items
    for tag in soup.find_all(["p", "li", "td", "span"]):
        txt = tag.get_text(" ", strip=True)
        if txt and len(txt) >= 25:
            chunks.append(txt)

    text = "\n".join(chunks)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# -----------------------------
# EXTRAÇÃO DE CAMPOS
# -----------------------------

COUNTRIES = [
    "Chile", "França", "France", "Itália", "Italia", "Spain", "Espanha",
    "Portugal", "Argentina", "Brasil", "Germany", "Alemanha",
    "United States", "USA", "Estados Unidos", "South Africa",
    "África do Sul", "New Zealand", "Nova Zelândia", "Australia", "Austrália"
]

REGIONS = [
    "Valle Central", "Maipo", "Colchagua", "Casablanca", "Maule",
    "Bordeaux", "Bourgogne", "Champagne", "Rhône", "Loire", "Alsace",
    "Piemonte", "Toscana", "Barolo", "Barbaresco", "Chianti",
    "Rioja", "Ribera del Duero", "Priorat", "Douro", "Dão",
    "Mosel", "Rheingau", "Mendoza", "Napa Valley", "Sonoma",
    "Marlborough", "Stellenbosch"
]

GRAPES = [
    "Merlot", "Cabernet Sauvignon", "Cabernet Franc", "Chardonnay",
    "Pinot Noir", "Sauvignon Blanc", "Riesling", "Syrah", "Shiraz",
    "Malbec", "Nebbiolo", "Sangiovese", "Tempranillo", "Carménère",
    "Carmenere", "Touriga Nacional", "Chenin Blanc", "Gewurztraminer",
    "Viognier", "Albariño", "Albarino", "Semillon", "Sémillon",
    "Petit Verdot", "Barbera", "Dolcetto", "Grenache", "Garnacha"
]

CLASSIFICATIONS = [
    "DOCG", "DOC", "AOC", "AOP", "IGP", "DOP", "IGT", "DO", "DOCa"
]


def normalize_spaces(text: str):
    text = text or ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_first_keyword(text: str, keywords: list):
    text_low = text.lower()
    for item in keywords:
        if item.lower() in text_low:
            return item
    return None


def regex_extract(patterns, text, flags=re.IGNORECASE):
    for pattern in patterns:
        m = re.search(pattern, text, flags)
        if m:
            val = m.group(1).strip(" .:-")
            if val:
                return normalize_spaces(val)
    return None


def extract_alcohol(text: str):
    patterns = [
        r"(?:alcool|álcool|alcohol)[^\d]{0,20}(\d{1,2}[.,]\d{1,2}\s?%?)",
        r"(\d{1,2}[.,]\d{1,2}\s?%?\s?(?:vol|abv))",
        r"(\d{1,2}[.,]\d{1,2}\s?%)"
    ]
    val = regex_extract(patterns, text)
    if not val:
        return None

    val = val.replace(",", ".")
    if "%" not in val:
        if "vol" in val.lower() or "abv" in val.lower():
            return val
        return f"{val}%"
    return val


def extract_vintage(text: str):
    m = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    return m.group(1) if m else None


def extract_producer(text: str, query: str = ""):
    patterns = [
        r"(?:producer|produtor|vinícola|vinicola|winery|bodega|cantina|domaine|producer:|produced by)\s*[:\-]?\s*([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇa-z0-9&'.,\- ]{3,80})",
        r"(?:by)\s+([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇa-z0-9&'.,\- ]{3,80})"
    ]
    val = regex_extract(patterns, text)
    if val:
        return val

    # fallback simples pelo query
    q = (query or "").lower()
    if "gato negro" in q:
        return "Viña San Pedro"
    return None


def extract_aroma(text: str):
    patterns = [
        r"(?:aroma|aromas|nose|bouquet)\s*[:\-]?\s*([^.\n]{20,300})",
        r"(?:notes of|notas de)\s*([^.\n]{20,300})"
    ]
    return regex_extract(patterns, text)


def extract_flavor(text: str):
    patterns = [
        r"(?:palate|boca|sabor|taste|flavor|flavour)\s*[:\-]?\s*([^.\n]{20,300})",
        r"(?:on the palate)\s*([^.\n]{20,300})"
    ]
    return regex_extract(patterns, text)


def extract_body(text: str):
    text_low = text.lower()
    if "full-bodied" in text_low or "full bodied" in text_low or "encorpado" in text_low:
        return "Encorpado"
    if "medium-bodied" in text_low or "medium bodied" in text_low or "corpo médio" in text_low:
        return "Médio"
    if "light-bodied" in text_low or "light bodied" in text_low or "leve" in text_low:
        return "Leve"
    return None


def extract_acidity(text: str):
    text_low = text.lower()
    if "high acidity" in text_low or "alta acidez" in text_low:
        return "Alta"
    if "medium acidity" in text_low or "acidez média" in text_low:
        return "Média"
    if "low acidity" in text_low or "baixa acidez" in text_low:
        return "Baixa"
    return None


def extract_tannin(text: str):
    text_low = text.lower()
    if "firm tannins" in text_low or "taninos firmes" in text_low:
        return "Firmes"
    if "soft tannins" in text_low or "taninos macios" in text_low or "smooth tannins" in text_low:
        return "Macios"
    if "medium tannins" in text_low or "taninos médios" in text_low:
        return "Médios"
    return None


def extract_oak(text: str):
    text_low = text.lower()
    if "oak" in text_low or "carvalho" in text_low or "barrel" in text_low or "barrica" in text_low:
        return "Há menção a madeira / barrica / carvalho"
    return None


def extract_soil(text: str):
    patterns = [
        r"(?:soil|soils|solo|solos)\s*[:\-]?\s*([^.\n]{20,300})",
        r"(?:grown on|planted on)\s*([^.\n]{20,200})"
    ]
    return regex_extract(patterns, text)


def extract_climate(text: str):
    patterns = [
        r"(?:climate|clima)\s*[:\-]?\s*([^.\n]{20,300})"
    ]
    return regex_extract(patterns, text)


def extract_aging(text: str):
    patterns = [
        r"(?:aged|aging|ageing|maturation|maturação|envelhecimento)\s*[:\-]?\s*([^.\n]{15,250})",
        r"(?:aged in)\s*([^.\n]{15,250})"
    ]
    return regex_extract(patterns, text)


def extract_classification(text: str):
    return find_first_keyword(text, CLASSIFICATIONS)


def extract_country(text: str):
    return find_first_keyword(text, COUNTRIES)


def extract_region(text: str):
    return find_first_keyword(text, REGIONS)


def extract_grape(text: str):
    return find_first_keyword(text, GRAPES)


def extract_page_fields(text: str, query: str = ""):
    if not text:
        return {}

    data = {
        "producer": extract_producer(text, query),
        "vintage": extract_vintage(text),
        "country": extract_country(text),
        "region": extract_region(text),
        "classification": extract_classification(text),
        "grape": extract_grape(text),
        "alcohol": extract_alcohol(text),
        "aroma": extract_aroma(text),
        "flavor": extract_flavor(text),
        "body": extract_body(text),
        "acidity": extract_acidity(text),
        "tannin": extract_tannin(text),
        "oak": extract_oak(text),
        "soil": extract_soil(text),
        "climate": extract_climate(text),
        "aging_rules": extract_aging(text),
    }

    # remove campos vazios
    return {k: v for k, v in data.items() if v not in (None, "", [])}


# -----------------------------
# BUSCA WEB COMPLETA
# -----------------------------

def search_wine_online(query: str, max_pages: int = 5):
    queries = [
        f'"{query}" wine',
       
