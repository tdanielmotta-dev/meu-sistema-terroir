import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote, urlparse, parse_qs

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WineIndex/1.0)"
}


def safe_get(url: str, timeout: int = 20):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception:
        return None


def unwrap_duckduckgo_url(url: str) -> str:
    if not url:
        return url
    if url.startswith("//"):
        url = "https:" + url

    try:
        parsed = urlparse(url)
        if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
            qs = parse_qs(parsed.query)
            if "uddg" in qs and qs["uddg"]:
                return unquote(qs["uddg"][0])
    except Exception:
        pass
    return url


def duckduckgo_search(query: str, max_results: int = 8):
    if not query:
        return []

    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    resp = safe_get(url, timeout=25)
    if not resp:
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    results = []

    for block in soup.select(".result"):
        a = block.select_one("a.result__a")
        if not a:
            continue

        title = a.get_text(" ", strip=True)
        raw_url = a.get("href", "").strip()
        final_url = unwrap_duckduckgo_url(raw_url)

        snippet_el = block.select_one(".result__snippet")
        snippet = snippet_el.get_text(" ", strip=True) if snippet_el else ""

        if title and final_url:
            results.append({
                "title": title,
                "url": final_url,
                "snippet": snippet
            })

        if len(results) >= max_results:
            break

    return results


def extract_page_text(url: str, max_paragraphs: int = 8):
    resp = safe_get(url, timeout=25)
    if not resp:
        return ""

    soup = BeautifulSoup(resp.text, "lxml")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    texts = []

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        texts.append(meta_desc.get("content", "").strip())

    og_desc = soup.find("meta", attrs={"property": "og:description"})
    if og_desc and og_desc.get("content"):
        texts.append(og_desc.get("content", "").strip())

    for p in soup.find_all(["p", "li"]):
        t = p.get_text(" ", strip=True)
        if len(t) >= 40:
            texts.append(t)
        if len(texts) >= max_paragraphs:
            break

    dedup = []
    seen = set()
    for t in texts:
        key = t.strip().lower()
        if key and key not in seen:
            dedup.append(t)
            seen.add(key)

    return "\n".join(dedup[:max_paragraphs])


def search_wine_online(query: str):
    q = f'"{query}" wine OR vinho OR vivino OR winery OR domaine OR cantina'
    results = duckduckgo_search(q, max_results=8)

    enriched = []
    for item in results[:5]:
        page_text = extract_page_text(item["url"], max_paragraphs=6)
        enriched.append({
            **item,
            "page_text": page_text
        })
    return enriched


def search_denomination_online(query: str):
    q = f'"{query}" appellation OR DOCG OR DOC OR AOC OR AOP OR DOP OR IGP OR terroir'
    results = duckduckgo_search(q, max_results=8)

    enriched = []
    for item in results[:5]:
        page_text = extract_page_text(item["url"], max_paragraphs=6)
        enriched.append({
            **item,
            "page_text": page_text
        })
    return enriched
