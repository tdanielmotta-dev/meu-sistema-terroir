from difflib import SequenceMatcher
from database import fetch_all_wines, fetch_all_denominations


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


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
        ])

        score = similarity(query, haystack)
        if query.lower() in haystack.lower():
            score += 0.35

        if score > best_score:
            best_score = score
            best = wine

    if best and best_score >= 0.35:
        best = dict(best)
        best["_score"] = round(best_score, 4)
        return best

    return None


def search_local_denomination(query: str):
    query = (query or "").strip()
    if not query:
        return None

    denoms = fetch_all_denominations()
    best = None
    best_score = 0.0

    for d in denoms:
        haystack = " ".join([
            str(d.get("country", "")),
            str(d.get("region", "")),
            str(d.get("denomination", "")),
            str(d.get("classification", "")),
            str(d.get("allowed_grapes", "")),
            str(d.get("notes", "")),
        ])

        score = similarity(query, haystack)
        if query.lower() in haystack.lower():
            score += 0.35

        if score > best_score:
            best_score = score
            best = d

    if best and best_score >= 0.35:
        best = dict(best)
        best["_score"] = round(best_score, 4)
        return best

    return None
