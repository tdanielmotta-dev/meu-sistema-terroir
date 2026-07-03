import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WineIndex/1.0; +https://streamlit.app)"
}


def safe_get(url: str, timeout: int = 15):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception:
        return None


def duckduckgo_search(query: str, max_results: int = 5):
    """
    Busca web simples via HTML do DuckDuckGo.
    Retorna lista de dicts com title/url/snippet.
    """
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
    """
    Tenta puxar um resumo bruto da página.
    """
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
    """
    Busca web específica do rótulo / vinho.
    """
    results = duckduckgo_search(f'"{query}" vinho OR wine OR winery OR domaine OR cantina', max_results=5)
    enriched = []

    for item in results[:3]:
        summary = extract_page_summary(item["url"], max_paragraphs=2)
        enriched.append({
            **item,
            "page_summary": summary
        })

    return enriched


def search_denomination_online(query: str):
    """
    Busca web específica da denominação / legislação / terroir.
    """
    results = duckduckgo_search(
        f'"{query}" appellation OR DOCG OR AOC OR DOP OR denominazione OR terroir',
        max_results=5
    )

    enriched = []
    for item in results[:3]:
        summary = extract_page_summary(item["url"], max_paragraphs=2)
        enriched.append({
            **item,
            "page_summary": summary
        })

    return enriched
