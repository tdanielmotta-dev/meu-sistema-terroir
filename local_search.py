from difflib import SequenceMatcher
from database import fetch_all_wines, fetch_all_denominations


def similarity(a: str, b: str) -> float:
    a = (a or "").lower()
    b = (b or "").lower()
    return SequenceMatcher(None, a, b).ratio()


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
            str(wine.get("wine_type", "")),
            str(wine.get("notes", "")),
        ])

        score = similarity(query, haystack)

        if query.lower() in haystack.lower():
            score += 0.35

        if score > best_score:
            best_score = score
            best = wine

    if best and best_score >= 0.30:
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

    for den in denoms:
        haystack = " ".join([
            str(den.get("country", "")),
            str(den.get("region", "")),
            str(den.get("denomination", "")),
            str(den.get("classification", "")),
            str(den.get("allowed_grapes", "")),
            str(den.get("aging_rules", "")),
            str(den.get("notes", "")),
        ])

        score = similarity(query, haystack)

        if query.lower() in haystack.lower():
            score += 0.35

        if score > best_score:
            best_score = score
            best = den

    if best and best_score >= 0.30:
        best = dict(best)
        best["_score"] = round(best_score, 4)
        return best

    return None
