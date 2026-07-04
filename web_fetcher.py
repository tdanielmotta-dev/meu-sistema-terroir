import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, parse_qs, unquote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WineIndex/1.0; +https://streamlit.app)"
}

GRAPES = [
    "Malbec", "Merlot", "Cabernet Sauvignon", "Cabernet Franc", "Pinot Noir",
    "Nebbiolo", "Chardonnay", "Sauvignon Blanc", "Syrah", "Carménère",
    "Tempranillo", "Sangiovese", "Grenache", "Gamay", "Riesling"
]

COUNTRIES = [
    "France", "França", "Italy", "Itália", "Chile", "Argentina", "Spain", "Espanha",
    "Portugal", "Brazil", "Brasil"
]

REGIONS = [
    "Bordeaux", "Piemonte", "Barolo", "Barbaresco", "Rioja", "Mendoza",
    "Central Valley", "Douro", "Champagne", "Burgundy", "Bourgogne", "Toscana",
    "Maipo", "Colchagua", "Uco Valley", "San Carlos"
]

DENOMS = ["DOCG", "DOC", "AOC", "AOP", "DO", "DOP", "IGP", "IG"]


def safe_get(url: str, timeout: int = 15):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception:
        return None


def normalize_ddg_url(url: str) -> str:
    if not url:
        return url
    if url.startswith("//"):
        url = "https:" + url
    if "duckduckgo.com/l/?" in url:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        uddg = qs.get("uddg")
        if uddg:
            return unquote(uddg[0])
    return url


def duckduckgo_search(query: str, max_results: int = 8):
    query = (query or "").strip()
    if not query:
        return []

    search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    resp = safe_get(search_url, timeout=20)
    if not resp:
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    results = []

    for a in soup.select("a.result__a"):
        title = a.get_text(" ", strip=True)
        url = normalize_ddg_url(a.get("href", "").strip())

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


def extract_page_summary(url: str, max_paragraphs: int = 3):
    resp = safe_get(url, timeout=20)
    if not resp:
        return ""

    soup = BeautifulSoup(resp.text, "lxml")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs = []
    for p in soup.find_all("p"):
        txt = p.get_text(" ", strip=True)
        if len(txt) >= 60:
            paragraphs.append(txt)
        if len(paragraphs) >= max_paragraphs:
            break

    return "\n\n".join(paragraphs[:max_paragraphs])


def search_wine_online(query: str):
    q = f'"{query}" wine vinho vivino winery producer producer tasting notes alcohol region'
    results = duckduckgo_search(q, max_results=8)

    enriched = []
    for item in results[:5]:
        summary = extract_page_summary(item["url"], max_paragraphs=2)
        enriched.append({
            **item,
            "page_summary": summary
        })

    return enriched


def search_denomination_online(query: str):
    q = f'"{query}" appellation DOCG DOC AOC AOP DO DOP IGP terroir legislation denomination'
    results = duckduckgo_search(q, max_results=8)

    enriched = []
    for item in results[:5]:
        summary = extract_page_summary(item["url"], max_paragraphs=2)
        enriched.append({
            **item,
            "page_summary": summary
        })

    return enriched


def extract_alcohol(text: str):
    m = re.search(r'(\d{1,2}(?:[.,]\d)?)\s*%(\s*vol)?', text, re.IGNORECASE)
    if m:
        return m.group(1).replace(",", ".") + "%"
    return ""


def extract_vintage(text: str):
    m = re.search(r'\b(19\d{2}|20\d{2})\b', text)
    return m.group(1) if m else ""


def extract_grape(text: str):
    for g in GRAPES:
        if g.lower() in text.lower():
            return g
    return ""


def extract_country(text: str):
    for c in COUNTRIES:
        if c.lower() in text.lower():
            return c
    return ""


def extract_region(text: str):
    for r in REGIONS:
        if r.lower() in text.lower():
            return r
    return ""


def extract_denomination(text: str):
    for d in DENOMS:
        if re.search(rf"\b{re.escape(d)}\b", text, re.IGNORECASE):
            return d.upper()
    return ""


def extract_simple_descriptor(text: str, keywords):
    low = text.lower()
    for k in keywords:
        if k.lower() in low:
            return k
    return ""


def parse_online_source(source_item: dict):
    title = source_item.get("title", "") or ""
    snippet = source_item.get("snippet", "") or ""
    summary = source_item.get("page_summary", "") or ""

    raw = " ".join([title, snippet, summary]).strip()

    parsed = {
        "alcohol": extract_alcohol(raw),
        "vintage": extract_vintage(raw),
        "grape": extract_grape(raw),
        "country": extract_country(raw),
        "region": extract_region(raw),
        "denomination": extract_denomination(raw),
        "aromas": "",
        "palate": "",
        "acidity": "",
        "soil": "",
        "climate": "",
        "terroir": "",
        "aging": "",
        "pairing": "",
        "raw_excerpt": raw[:3000]
    }

    aroma_words = ["black fruit", "red fruit", "plum", "cherry", "oak", "vanilla", "spice", "floral", "frutas vermelhas", "ameixa"]
    palate_words = ["medium-bodied", "full-bodied", "smooth", "soft tannins", "fresh", "frutado", "macio"]
    acidity_words = ["high acidity", "medium acidity", "acidez média", "alta acidez", "média acidez"]
    climate_words = ["mediterranean", "continental", "maritime", "mediterrâneo", "continental", "marítimo"]
    soil_words = ["limestone", "clay", "gravel", "calcareous", "argilo", "calcário", "cascalho"]

    for word in aroma_words:
        if word.lower() in raw.lower():
            parsed["aromas"] = word
            break

    for word in palate_words:
        if word.lower() in raw.lower():
            parsed["palate"] = word
            break

    for word in acidity_words:
        if word.lower() in raw.lower():
            parsed["acidity"] = word
            break

    for word in climate_words:
        if word.lower() in raw.lower():
            parsed["climate"] = word
            break

    for word in soil_words:
        if word.lower() in raw.lower():
            parsed["soil"] = word
            break

    # bloco especial para Vivino / textos com tasting notes
    vivino_oak = re.search(r"(\d+\s+mentions of oaky notes.*?)(?:\.|$)", raw, re.IGNORECASE)
    if vivino_oak:
        parsed["aging"] = vivino_oak.group(1).strip()

    return parsed
