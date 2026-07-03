import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
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

    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    resp = safe_get(url, timeout=25)
    if not resp:
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    results = []

    for a in soup.select("a.result__a"):
        title = a.get_text(" ", strip=True)
        href = a.get("href", "").strip()

        snippet = ""
        wrapper = a.find_parent("div", class_="result")
        if wrapper:
            sn = wrapper.select_one(".result__snippet")
            if sn:
                snippet = sn.get_text(" ", strip=True)

        if title and href:
            results.append({
                "title": title,
                "url": href,
                "snippet": snippet
            })

        if len(results) >= max_results:
            break

    return results


def build_search_queries(query: str, parsed: dict):
    base = (query or "").strip()
    q = []

    q.append(f'"{base}" wine')
    q.append(f'"{base}" vinho')
    q.append(f'"{base}" vivino')
    q.append(f'"{base}" winery')
    q.append(f'"{base}" technical sheet')
    q.append(f'"{base}" ficha técnica')
    q.append(f'"{base}" alcohol grape region')

    grape = parsed.get("grape")
    vintage = parsed.get("vintage")
    denomination = parsed.get("denomination")

    if grape:
        q.append(f'"{base}" "{grape}" wine')
    if vintage:
        q.append(f'"{base}" "{vintage}" wine')
    if denomination:
        q.append(f'"{base}" "{denomination}"')

    # remove duplicadas preservando ordem
    unique = []
    seen = set()
    for item in q:
        if item not in seen:
            seen.add(item)
            unique.append(item)

    return unique[:8]


def search_wine_sources(query: str, parsed: dict):
    final_results = []
    seen_urls = set()

    for sq in build_search_queries(query, parsed):
        items = duckduckgo_search(sq, max_results=5)
        for item in items:
            url = item.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                final_results.append(item)

    return final_results[:15]
