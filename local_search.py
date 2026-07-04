from difflib import SequenceMatcher
from database import fetch_all_wines

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()

def search_local_wine(query: str):
    query = (query or "").strip()
    if not query:
        return None

    wines = fetch_all_wines()
    best = None
    best_score = 0.0

    for wine in wines:
        haystack = " ".join([
            str(wine.get("producer", "")),
            str(wine.get("wine_name", "")),
            str(wine.get("vintage", "")),
            str(wine.get("grape", "")),
            str(wine.get("region", "")),
            str(wine.get("country", "")),
            str(wine.get("denomination", "")),
            str(wine.get("classification", "")),
        ])

        score = similarity(query, haystack)

        if query.lower() in haystack.lower():
            score += 0.35

        if score > best_score:
            best_score = score
            best = dict(wine)

    if best and best_score >= 0.35:
        best["_score"] = round(best_score, 4)
        return best

    return None
