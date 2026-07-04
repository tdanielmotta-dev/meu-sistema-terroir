import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote, urlparse, parse_qs

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WineIndex/1.0; +https://streamlit.app)"
}


def safe_get(url: str, timeout: int = 20):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception:
        return None


def normalize_result_url(url: str):
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


def duckduckgo_search(query: str, max_results: int = 6):
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
        url = a.get("href", "").strip()
        url = normalize_result_url(url)

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


def extract_page_summary(url: str, max_paragraphs: int = 4):
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


def _extract_first(patterns, text):
    for p in patterns:
        m = re.search(p, text, flags=re.I)
        if m:
            return m.group(1).strip()
    return ""


def parse_online_wine_text(text: str):
    raw = text or ""
    txt = " ".join(raw.split())

    data = {
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
        "raw_excerpt": txt[:2500]
    }

    vintage = _extract_first([r"\b(19\d{2}|20\d{2})\b"], txt)
    if vintage:
        data["vintage"] = vintage

    alcohol = _extract_first([
        r"(\d{1,2}(?:[.,]\d)?)\s*%",
        r"alcohol[^0-9]{0,10}(\d{1,2}(?:[.,]\d)?)",
        r"abv[^0-9]{0,10}(\d{1,2}(?:[.,]\d)?)"
    ], txt)
    if alcohol:
        data["alcohol"] = alcohol.replace(",", ".") + "%"

    grape_map = [
        "Cabernet Sauvignon", "Cabernet Franc", "Merlot", "Malbec", "Pinot Noir",
        "Syrah", "Shiraz", "Nebbiolo", "Sangiovese", "Tempranillo", "Carmenere",
        "Chardonnay", "Sauvignon Blanc", "Riesling", "Gewurztraminer",
        "Chenin Blanc", "Viognier", "Grenache", "Garnacha", "Touriga Nacional", "Tannat"
    ]
    lower = txt.lower()
    for g in grape_map:
        if g.lower() in lower:
            data["grape"] = g
            break

    country_map = [
        "France", "Italy", "Spain", "Portugal", "Chile", "Argentina",
        "Brazil", "Uruguay", "Germany", "Australia", "United States"
    ]
    for c in country_map:
        if c.lower() in lower:
            data["country"] = c
            break

    region_map = [
        "Bordeaux", "Burgundy", "Champagne", "Piemonte", "Toscana", "Rioja",
        "Douro", "Central Valley", "Mendoza", "Barolo", "Barbaresco", "Chablis",
        "Sauternes", "Médoc", "Uco Valley", "San Carlos"
    ]
    for r in region_map:
        if r.lower() in lower:
            if not data["region"]:
                data["region"] = r
            else:
                data["subregion"] = r

    denom_patterns = [
        r"\b([A-Z][A-Za-zÀ-ÿ' -]{2,}\sDOCG)\b",
        r"\b([A-Z][A-Za-zÀ-ÿ' -]{2,}\sDOC)\b",
        r"\b([A-Z][A-Za-zÀ-ÿ' -]{2,}\sAOC)\b",
        r"\b([A-Z][A-Za-zÀ-ÿ' -]{2,}\sDOP)\b",
        r"\b([A-Z][A-Za-zÀ-ÿ' -]{2,}\sIGP)\b",
        r"\b([A-Z][A-Za-zÀ-ÿ' -]{2,}\sDO)\b",
    ]
    for p in denom_patterns:
        m = re.search(p, txt)
        if m:
            data["denomination"] = m.group(1).strip()
            break

    if not data["denomination"]:
        if re.search(r"\bDOCG\b", txt, flags=re.I):
            data["classification"] = "DOCG"
        elif re.search(r"\bDOC\b", txt, flags=re.I):
            data["classification"] = "DOC"
        elif re.search(r"\bAOC\b", txt, flags=re.I):
            data["classification"] = "AOC"
        elif re.search(r"\bDOP\b", txt, flags=re.I):
            data["classification"] = "DOP"
        elif re.search(r"\bIGP\b", txt, flags=re.I):
            data["classification"] = "IGP"
        elif re.search(r"\bDO\b", txt, flags=re.I):
            data["classification"] = "DO"

    wine_type_map = ["Red wine", "White wine", "Rosé wine", "Sparkling wine", "Dessert wine"]
    for wt in wine_type_map:
        if wt.lower() in lower:
            if "red" in wt.lower():
                data["wine_type"] = "Tinto"
            elif "white" in wt.lower():
                data["wine_type"] = "Branco"
            elif "rosé" in wt.lower() or "rose" in wt.lower():
                data["wine_type"] = "Rosé"
            elif "sparkling" in wt.lower():
                data["wine_type"] = "Espumante"
            elif "dessert" in wt.lower():
                data["wine_type"] = "Doce"
            break

    aroma_match = _extract_first([
        r"aromas?[:\-]\s*([^\.]{10,250})",
        r"notes? of\s+([^\.]{10,250})",
    ], txt)
    if aroma_match:
        data["aromas"] = aroma_match

    palate_match = _extract_first([
        r"palate[:\-]\s*([^\.]{10,250})",
        r"on the palate[,:\-]?\s*([^\.]{10,250})",
    ], txt)
    if palate_match:
        data["palate"] = palate_match

    acidity_match = _extract_first([
        r"(high acidity|medium acidity|low acidity)",
        r"(alta acidez|média acidez|baixa acidez)"
    ], txt)
    if acidity_match:
        data["acidity"] = acidity_match

    body_match = _extract_first([
        r"(full-bodied|medium-bodied|light-bodied)",
        r"(encorpado|médio corpo|leve corpo)"
    ], txt)
    if body_match:
        data["body"] = body_match

    soil_match = _extract_first([
        r"soil[s]?[:\-]\s*([^\.]{10,250})",
        r"grown on\s+([^\.]{10,250})"
    ], txt)
    if soil_match:
        data["soil"] = soil_match

    climate_match = _extract_first([
        r"climate[:\-]\s*([^\.]{10,250})",
        r"(mediterranean climate|continental climate|maritime climate)"
    ], txt)
    if climate_match:
        data["climate"] = climate_match

    terroir_match = _extract_first([
        r"terroir[:\-]\s*([^\.]{10,250})"
    ], txt)
    if terroir_match:
        data["terroir"] = terroir_match

    aging_match = _extract_first([
        r"aged? in\s+([^\.]{5,250})",
        r"oak[^\.]{0,200}",
        r"barrel[^\.]{0,200}",
        r"matured? in\s+([^\.]{5,250})"
    ], txt)
    if aging_match:
        data["aging"] = aging_match

    pairing_match = _extract_first([
        r"pair(?:ing)?[:\-]\s*([^\.]{10,250})",
        r"pairs well with\s+([^\.]{10,250})"
    ], txt)
    if pairing_match:
        data["pairing"] = pairing_match

    return data


def search_wine_online(query: str):
    queries = [
        f'"{query}" wine',
        f'"{query}" vivino',
        f'"{query}" winery',
        f'"{query}" producer',
    ]

    seen = set()
    merged = []

    for q in queries:
        for item in duckduckgo_search(q, max_results=4):
            url = item["url"]
            if url in seen:
                continue
            seen.add(url)

            summary = extract_page_summary(url, max_paragraphs=3)
            combined_text = f"{item.get('title', '')}\n{item.get('snippet', '')}\n{summary}"
            parsed = parse_online_wine_text(combined_text)

            merged.append({
                **item,
                "page_summary": summary,
                "parsed_data": parsed
            })

            if len(merged) >= 8:
                return merged

    return merged


def search_denomination_online(query: str):
    queries = [
        f'"{query}" appellation',
        f'"{query}" DOCG OR DOC OR AOC OR DOP OR IGP',
        f'"{query}" denomination wine',
        f'"{query}" terroir regulation',
    ]

    seen = set()
    merged = []

    for q in queries:
        for item in duckduckgo_search(q, max_results=4):
            url = item["url"]
            if url in seen:
                continue
            seen.add(url)

            summary = extract_page_summary(url, max_paragraphs=3)
            combined_text = f"{item.get('title', '')}\n{item.get('snippet', '')}\n{summary}"
            parsed = parse_online_wine_text(combined_text)

            merged.append({
                **item,
                "page_summary": summary,
                "parsed_data": parsed
            })

            if len(merged) >= 8:
                return merged

    return merged
