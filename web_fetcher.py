import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WineIndexOmega/Final; +https://streamlit.app)"
}

def safe_get(url: str, timeout: int = 20):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception:
        return None

def normalize_ddg_link(url: str):
    if not url:
        return url
    if url.startswith("//"):
        return "https:" + url
    return url

def duckduckgo_search(query: str, max_results: int = 8):
    q = (query or "").strip()
    if not q:
        return []

    url = f"https://html.duckduckgo.com/html/?q={quote(q)}"
    resp = safe_get(url, timeout=25)
    if not resp:
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    results = []

    for result in soup.select(".result"):
        a = result.select_one("a.result__a")
        if not a:
            continue

        title = a.get_text(" ", strip=True)
        href = normalize_ddg_link(a.get("href", "").strip())

        snippet = ""
        sn = result.select_one(".result__snippet")
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
    normalized = (parsed.get("normalized_query") or query or "").strip()

    queries = [
        f'"{normalized}" wine',
        f'"{normalized}" vinho',
        f'"{normalized}" vivino',
        f'"{normalized}" wine-searcher',
        f'"{normalized}" technical sheet',
        f'"{normalized}" fiche technique',
        f'"{normalized}" producer',
        f'"{normalized}" winery',
        f'"{normalized}" domaine',
        f'"{normalized}" cantina',
        f'"{normalized}" tasting notes',
        f'"{normalized}" alcohol',
        f'"{normalized}" region',
    ]

    if parsed.get("region"):
        queries.append(f'"{normalized}" "{parsed["region"]}" wine')

    if parsed.get("grape"):
        queries.append(f'"{normalized}" "{parsed["grape"]}"')

    # dedup
    seen = set()
    out = []
    for q in queries:
        if q.lower() not in seen:
            out.append(q)
            seen.add(q.lower())
    return out

def search_wine_online(query: str, parsed: dict, per_query_results: int = 4, max_total: int = 18):
    all_results = []
    seen_urls = set()

    queries = build_search_queries(query, parsed)

    for q in queries:
        results = duckduckgo_search(q, max_results=per_query_results)
        for item in results:
            url = item.get("url", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            item["search_query"] = q
            all_results.append(item)
            if len(all_results) >= max_total:
                return all_results

    return all_results
