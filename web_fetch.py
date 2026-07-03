import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WineIndex/1.0)"
}


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


def extract_page_summary(url: str, max_paragraphs: int = 3):
    resp = safe_get(url)
    if not resp:
        return ""

    soup = BeautifulSoup(resp.text, "lxml")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs = []
    for p in soup.find_all("p"):
        txt = p.get_text(" ", strip=True)
        if len(txt) >= 80:
            paragraphs.append(txt)
        if len(paragraphs) >= max_paragraphs:
            break

    return "\n\n".join(paragraphs[:max_paragraphs])


def search_wine_online(query: str):
    queries = [
        f'"{query}" wine',
        f'"{query}" vinho',
        f'"{query}" winery',
        f'"{query}" tasting notes',
    ]

    final = []
    seen = set()

    for q in queries:
        results = duckduckgo_search(q, max_results=4)
        for item in results:
            url = item.get("url", "")
            if url in seen:
                continue
            seen.add(url)
            item["page_summary"] = extract_page_summary(url, max_paragraphs=2)
            final.append(item)
            if len(final) >= 6:
                return final

    return final


def search_denomination_online(query: str):
    queries = [
        f'"{query}" appellation terroir',
        f'"{query}" DOCG AOC DO DOC',
        f'"{query}" wine region soil climate grapes',
    ]

    final = []
    seen = set()

    for q in queries:
        results = duckduckgo_search(q, max_results=4)
        for item in results:
            url = item.get("url", "")
            if url in seen:
                continue
            seen.add(url)
            item["page_summary"] = extract_page_summary(url, max_paragraphs=2)
            final.append(item)
            if len(final) >= 6:
                return final

    return final
