import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WineIndex/1.0)"
}

# --------------------------------------------------
# BASES / LISTAS
# --------------------------------------------------

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
    "Petit Verdot", "Barbera", "Dolcetto", "Grenache", "Garnacha",
    "Pinot Grigio", "Moscato"
]

CLASSIFICATIONS = [
    "DOCG", "DOC", "AOC", "AOP", "IGP", "DOP", "IGT", "DO", "DOCa"
]

OFFICIAL_DENOMINATION_HINTS = [
    "consorzio", "consorzio tutela", "civc", "inao", "docg", "disciplinare",
    "appellation", "denomination", "denominazione", "consejo regulador",
    "official", "regulation", "regolamento", "cahier des charges"
]


# --------------------------------------------------
# UTILIDADES
# --------------------------------------------------

def normalize_spaces(text: str):
    text = text or ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_first_keyword(text: str, keywords: list):
    low = (text or "").lower()
    for item in keywords:
        if item.lower() in low:
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

    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        chunks.append(meta.get("content", "").strip())

    og_desc = soup.find("meta", attrs={"property": "og:description"})
    if og_desc and og_desc.get("content"):
        chunks.append(og_desc.get("content", "").strip())

    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        chunks.append(og_title.get("content", "").strip())

    for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "td", "span"]):
        txt = tag.get_text(" ", strip=True)
        if txt and len(txt) >= 20:
            chunks.append(txt)

    text = "\n".join(chunks)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# --------------------------------------------------
# EXTRAÇÕES GENÉRICAS
# --------------------------------------------------

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
    if "%" not in val and "vol" not in val.lower() and "abv" not in val.lower():
        val = f"{val}%"
    return val


def extract_vintage(text: str):
    m = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    return m.group(1) if m else None


def extract_producer(text: str, query: str = ""):
    patterns = [
        r"(?:producer|produtor|vinícola|vinicola|winery|bodega|cantina|domaine|produced by)\s*[:\-]?\s*([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇa-z0-9&'.,\- ]{3,80})",
        r"(?:by)\s+([A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇa-z0-9&'.,\- ]{3,80})"
    ]
    return regex_extract(patterns, text)


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
    low = text.lower()
    if "full-bodied" in low or "full bodied" in low or "encorpado" in low:
        return "Encorpado"
    if "medium-bodied" in low or "medium bodied" in low or "corpo médio" in low:
        return "Médio"
    if "light-bodied" in low or "light bodied" in low or "leve" in low:
        return "Leve"
    return None


def extract_acidity(text: str):
    low = text.lower()
    if "high acidity" in low or "alta acidez" in low:
        return "Alta"
    if "medium acidity" in low or "acidez média" in low:
        return "Média"
    if "low acidity" in low or "baixa acidez" in low:
        return "Baixa"
    return None


def extract_tannin(text: str):
    low = text.lower()
    if "firm tannins" in low or "taninos firmes" in low:
        return "Firmes"
    if "soft tannins" in low or "smooth tannins" in low or "taninos macios" in low:
        return "Macios"
    if "medium tannins" in low or "taninos médios" in low:
        return "Médios"
    return None


def extract_oak(text: str):
    low = text.lower()
    if "oak" in low or "carvalho" in low or "barrel" in low or "barrica" in low:
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


def extract_allowed_grapes(text: str):
    patterns = [
        r"(?:allowed grapes|permitted grapes|grapes permitted|vitigni ammessi|uvas permitidas)\s*[:\-]?\s*([^.\n]{10,400})"
    ]
    return regex_extract(patterns, text)


def extract_min_alcohol(text: str):
    patterns = [
        r"(?:minimum alcohol|min alcohol|alcool minimum|alcool minimo|álcool mínimo)\s*[:\-]?\s*([^.\n]{3,40})"
    ]
    return regex_extract(patterns, text)


def generic_extract_fields(text: str, query: str = ""):
    if not text:
        return {}

    data = {
        "producer": extract_producer(text, query),
        "vintage": extract_vintage(text),
        "country": find_first_keyword(text, COUNTRIES),
        "region": find_first_keyword(text, REGIONS),
        "classification": find_first_keyword(text, CLASSIFICATIONS),
        "grape": find_first_keyword(text, GRAPES),
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
        "allowed_grapes": extract_allowed_grapes(text),
        "min_alcohol": extract_min_alcohol(text),
    }
    return {k: v for k, v in data.items() if v not in (None, "", [])}


# --------------------------------------------------
# DETECÇÃO DE FONTE
# --------------------------------------------------

def detect_source_type(url: str, title: str = "", snippet: str = "", page_text: str = ""):
    joined = " ".join([url or "", title or "", snippet or "", page_text[:2500] or ""]).lower()

    if "vivino" in joined:
        return "vivino"

    # tenta achar sites de produtor / winery / bodega / cantina / domaine / importadora
    winery_words = ["winery", "bodega", "vinícola", "vinicola", "cantina", "domaine", "estate", "vineyards"]
    if any(w in joined for w in winery_words):
        return "producer"

    if any(w in joined for w in OFFICIAL_DENOMINATION_HINTS):
        return "official_denomination"

    return "generic"


# --------------------------------------------------
# PARSER VIVINO
# --------------------------------------------------

def parse_vivino_page(title: str, snippet: str, text: str, query: str = ""):
    base = generic_extract_fields(text, query=query)

    # tenta enriquecer com heurísticas comuns de página do Vivino
    joined = "\n".join([title or "", snippet or "", text or ""])

    if not base.get("grape"):
        base["grape"] = find_first_keyword(joined, GRAPES)

    if not base.get("country"):
        base["country"] = find_first_keyword(joined, COUNTRIES)

    if not base.get("region"):
        base["region"] = find_first_keyword(joined, REGIONS)

    # descrição sensorial no Vivino costuma ter texto corrido de review/description
    if not base.get("aroma"):
        aroma = regex_extract([
            r"(?:aromas? of|notas? de)\s*([^.\n]{20,250})"
        ], joined)
        if aroma:
            base["aroma"] = aroma

    if not base.get("body"):
        low = joined.lower()
        if "bold" in low:
            base["body"] = "Encorpado"
        elif "smooth" in low or "medium-bodied" in low:
            base["body"] = "Médio"

    if not base.get("acidity"):
        low = joined.lower()
        if "high acidity" in low:
            base["acidity"] = "Alta"
        elif "medium acidity" in low:
            base["acidity"] = "Média"

    base["source_type"] = "vivino"
    return base


# --------------------------------------------------
# PARSER PRODUTOR / IMPORTADORA / WINERY
# --------------------------------------------------

def parse_producer_page(title: str, snippet: str, text: str, query: str = ""):
    base = generic_extract_fields(text, query=query)
    joined = "\n".join([title or "", snippet or "", text or ""])

    # ficha técnica / vinificação / amadurecimento / harmonização
    tech_patterns = {
        "producer": [
            r"(?:producer|produtor|vinícola|vinicola|winery|bodega|domaine)\s*[:\-]?\s*([^.\n]{3,120})"
        ],
        "aging_rules": [
            r"(?:aging|ageing|maturation|maturação|envelhecimento|amadurecimento)\s*[:\-]?\s*([^.\n]{15,300})",
            r"(?:oak aging|aged in oak|matured in)\s*([^.\n]{15,300})"
        ],
        "soil": [
            r"(?:soil|solos?|terroir)\s*[:\-]?\s*([^.\n]{20,300})"
        ],
        "climate": [
            r"(?:climate|clima)\s*[:\-]?\s*([^.\n]{20,300})"
        ],
        "flavor": [
            r"(?:palate|boca|taste|flavor)\s*[:\-]?\s*([^.\n]{20,300})"
        ],
        "aroma": [
            r"(?:aroma|nose|bouquet)\s*[:\-]?\s*([^.\n]{20,300})"
        ]
    }

    for field, patterns in tech_patterns.items():
        if not base.get(field):
            val = regex_extract(patterns, joined)
            if val:
                base[field] = val

    base["source_type"] = "producer"
    return base


# --------------------------------------------------
# PARSER DENOMINAÇÃO OFICIAL / REGIÃO OFICIAL
# --------------------------------------------------

def parse_official_denomination_page(title: str, snippet: str, text: str, query: str = ""):
    base = generic_extract_fields(text, query=query)
    joined = "\n".join([title or "", snippet or "", text or ""])

    # foco em classificação, uvas permitidas, álcool mínimo, regras de envelhecimento
    if not base.get("classification"):
        base["classification"] = find_first_keyword(joined, CLASSIFICATIONS)

    if not base.get("allowed_grapes"):
        base["allowed_grapes"] = extract_allowed_grapes(joined)

    if not base.get("min_alcohol"):
        base["min_alcohol"] = extract_min_alcohol(joined)

    if not base.get("aging_rules"):
        base["aging_rules"] = regex_extract([
            r"(?:aging|ageing|maturation|maturação|envelhecimento|required aging|minimum aging)\s*[:\-]?\s*([^.\n]{15,300})"
        ], joined)

    if not base.get("soil"):
        base["soil"] = regex_extract([
            r"(?:soil|solos?|terroir)\s*[:\-]?\s*([^.\n]{20,300})"
        ], joined)

    if not base.get("climate"):
        base["climate"] = regex_extract([
            r"(?:climate|clima)\s*[:\-]?\s*([^.\n]{20,300})"
        ], joined)

    base["source_type"] = "official_denomination"
    return base


# --------------------------------------------------
# PIPELINE DE EXTRAÇÃO POR PÁGINA
# --------------------------------------------------

def parse_page_by_source(item: dict, query: str = ""):
    title = item.get("title", "")
    snippet = item.get("snippet", "")
    url = item.get("url", "")
    text = item.get("page_text", "")

    source_type = detect_source_type(url, title, snippet, text)

    if source_type == "vivino":
        extracted = parse_vivino_page(title, snippet, text, query=query)
    elif source_type == "producer":
        extracted = parse_producer_page(title, snippet, text, query=query)
    elif source_type == "official_denomination":
        extracted = parse_official_denomination_page(title, snippet, text, query=query)
    else:
        extracted = generic_extract_fields(text, query=query)
        extracted["source_type"] = "generic"

    return extracted


# --------------------------------------------------
# BUSCA WEB
# --------------------------------------------------

def search_wine_online(query: str, max_pages: int = 6):
    queries = [
        f'"{query}" site:vivino.com',
        f'"{query}" wine',
        f'"{query}" vinho',
        f'"{query}" ficha técnica',
        f'"{query}" winery',
        f'"{query}" producer'
    ]

    final = []
    seen = set()

    for q in queries:
        results = duckduckgo_search(q, max_results=5)

        for item in results:
            url = item.get("url", "")
            if not url or url in seen:
                continue
            seen.add(url)

            page_text = extract_page_text(url)
            enriched = {
                "title": item.get("title"),
                "url": url,
                "snippet": item.get("snippet"),
                "page_text": page_text[:20000]
            }
            enriched["extracted"] = parse_page_by_source(enriched, query=query)
            final.append(enriched)

            if len(final) >= max_pages:
                return final

    return final


def search_denomination_online(query: str, max_pages: int = 6):
    queries = [
        f'"{query}" DOC DOCG AOC DOP',
        f'"{query}" appellation official',
        f'"{query}" disciplinare',
        f'"{query}" consorzio',
        f'"{query}" terroir grapes climate'
    ]

    final = []
    seen = set()

    for q in queries:
        results = duckduckgo_search(q, max_results=5)

        for item in results:
            url = item.get("url", "")
            if not url or url in seen:
                continue
            seen.add(url)

            page_text = extract_page_text(url)
            enriched = {
                "title": item.get("title"),
                "url": url,
                "snippet": item.get("snippet"),
                "page_text": page_text[:20000]
            }
            enriched["extracted"] = parse_page_by_source(enriched, query=query)
            final.append(enriched)

            if len(final) >= max_pages:
                return final

    return final
