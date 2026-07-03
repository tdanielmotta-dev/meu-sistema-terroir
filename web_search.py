import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

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


def duckduckgo_search(query: str, max_results: int = 8):
    query = (query or "").strip()
    if not query:
        return []

    search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    resp = safe_get(search_url, timeout=25)
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


def extract_page_summary(url: str, max_paragraphs: int = 4):
    resp = safe_get(url, timeout=25)
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
    queries = [
        f'"{query}" vinho OR wine OR winery OR producer OR tasting notes',
        f'"{query}" alcohol OR vintage OR grape OR region',
        f'"{query}" vivino OR wine-searcher OR winery'
    ]

    merged = []
    seen = set()

    for q in queries:
        res = duckduckgo_search(q, max_results=5)
        for item in res:
            url = item.get("url", "")
            if url and url not in seen:
                seen.add(url)
                merged.append(item)

    enriched = []
    for item in merged[:8]:
        summary = extract_page_summary(item["url"], max_paragraphs=3)
        enriched.append({
            **item,
            "page_summary": summary
        })

    return enriched


def search_denomination_online(query: str):
    queries = [
        f'"{query}" appellation OR DOCG OR DOC OR AOC OR DOP OR IGP',
        f'"{query}" terroir OR soil OR climate OR grapes',
        f'"{query}" official denomination wine region'
    ]

    merged = []
    seen = set()

    for q in queries:
        res = duckduckgo_search(q, max_results=5)
        for item in res:
            url = item.get("url", "")
            if url and url not in seen:
                seen.add(url)
                merged.append(item)

    enriched = []
    for item in merged[:8]:
        summary = extract_page_summary(item["url"], max_paragraphs=3)
        enriched.append({
            **item,
            "page_summary": summary
        })

    return enriched
