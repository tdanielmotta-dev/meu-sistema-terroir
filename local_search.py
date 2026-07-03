from difflib import SequenceMatcher
from database import fetch_all_wines, fetch_all_denominations, fetch_all_producers


def similarity(a: str, b: str) -> float:
    a = (a or "").lower()
    b = (b or "").lower()
    return SequenceMatcher(None, a, b).ratio()


def _score_query_against_text(query: str, haystack: str) -> float:
    query = (query or "").strip()
    haystack = (haystack or "").strip()

    if not query or not haystack:
        return 0.0

    score = similarity(query, haystack)

    if query.lower() in haystack.lower():
        score += 0.35

    query_words = [w for w in query.lower().split() if len(w) >= 3]
    haystack_lower = haystack.lower()

    hits = sum(1 for w in query_words if w in haystack_lower)
    if query_words:
        score += min(0.25, hits * 0.05)

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
            str(wine.get("wine_type", "")),
            str(wine.get("notes", "")),
        ])

        score = _score_query_against_text(query, haystack)

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

        score = _score_query_against_text(query, haystack)

        if score > best_score:
            best_score = score
            best = d

    if best and best_score >= 0.35:
        best["_score"] = round(best_score, 4)
        return best

    return None


def search_local_producer(query: str):
    query = (query or "").strip()
    if not query:
        return None

    producers = fetch_all_producers()
    best = None
    best_score = 0.0

    for p in producers:
        haystack = " ".join([
            str(p.get("producer_name", "")),
            str(p.get("country", "")),
            str(p.get("region", "")),
            str(p.get("subregion", "")),
            str(p.get("website", "")),
            str(p.get("notes", "")),
        ])

        score = _score_query_against_text(query, haystack)

        if score > best_score:
            best_score = score
            best = p

    if best and best_score >= 0.35:
        best["_score"] = round(best_score, 4)
        return best

    return None
