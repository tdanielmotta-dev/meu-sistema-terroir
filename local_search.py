from difflib import SequenceMatcher
from database import fetch_all_wines, fetch_all_denominations
from knowledge_base import KNOWLEDGE_BASE


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
            str(wine.get("subregion", "")),
            str(wine.get("country", "")),
            str(wine.get("denomination", "")),
        ]).strip()

        score = similarity(query, haystack)
        if query.lower() in haystack.lower():
            score += 0.35

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
            str(d.get("subregion", "")),
            str(d.get("denomination", "")),
            str(d.get("classification", "")),
            str(d.get("allowed_grapes", "")),
            str(d.get("notes", "")),
        ]).strip()

        score = similarity(query, haystack)
        if query.lower() in haystack.lower():
            score += 0.35

        if score > best_score:
            best_score = score
            best = d

    if best and best_score >= 0.35:
        best["_score"] = round(best_score, 4)
        return best

    return None


def search_knowledge_base(query: str):
    query = (query or "").strip().lower()
    if not query:
        return []

    matches = []

    for item in KNOWLEDGE_BASE:
        score = 0.0
        aliases = item.get("aliases", [])
        hay_parts = aliases + [
            item.get("producer", ""),
            item.get("wine_name", ""),
            item.get("vintage", ""),
            item.get("grape", ""),
            item.get("country", ""),
            item.get("region", ""),
            item.get("subregion", ""),
            item.get("denomination", ""),
        ]
        haystack = " ".join([str(x) for x in hay_parts if x]).lower()

        score = similarity(query, haystack)
        if query in haystack:
            score += 0.45

        if score >= 0.35:
            obj = dict(item)
            obj["_score"] = round(score, 4)
            matches.append(obj)

    matches.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return matches
