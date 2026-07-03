import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_web(query: str, max_results: int = 5):
    url = "https://html.duckduckgo.com/html/"
    try:
        resp = requests.post(url, data={"q": query}, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        return {
            "query": query,
            "results": [],
            "error": str(e)
        }

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for a in soup.select(".result__a")[:max_results]:
        title = a.get_text(" ", strip=True)
        href = a.get("href")
        results.append({
            "title": title,
            "url": href
        })

    return {
        "query": query,
        "results": results,
        "error": None
    }
