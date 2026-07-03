from difflib import SequenceMatcher
from database import fetch_all_wines, fetch_all_denominations


def similarity(a: str, b: str) -> float:
    a = (a or "").lower().strip()
    b = (b or "").lower().strip()
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def score_match(query: str, haystack: str, bonus_terms=None) -> float:
    score = similarity(query, haystack)

    query_low = query.lower()
    hay_low = haystack.lower()

    if query_low in hay_low:
        score += 0.35

    if bonus_terms:
        for term in bonus_terms:
            if term and str(term).lower() in hay_low:
                score += 0.08

    return score


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
            str(wine.get("wine_type", "")),
            str(wine.get("notes", "")),
        ])

        bonus = [
            wine.get("producer"),
            wine.get("wine_name"),
            wine.get("denomination"),
            wine.get("region"),
            wine.get("classification"),
        ]

        score = score_match(query, haystack, bonus_terms=bonus)

        if score > best_score:
            best_score = score
            best = wine

    if best and best_score >= 0.35:
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
            str(d.get("aging_rules", "")),
            str(d.get("notes", "")),
        ])

        bonus = [
            d.get("country"),
            d.get("region"),
            d.get("denomination"),
            d.get("classification"),
        ]

        score = score_match(query, haystack, bonus_terms=bonus)

        if score > best_score:
            best_score = score
            best = d

    if best and best_score >= 0.35:
        best["_score"] = round(best_score, 4)
        return best

    return None
