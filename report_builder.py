from difflib import SequenceMatcher

from database import fetch_all_wines, fetch_all_denominations
from parser_engine import parse_wine_query
from web_fetch import search_wine_online, search_denomination_online
from knowledge_base import get_knowledge_matches


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
            str(wine.get("notes", "")),
        ])

        score = similarity(query, haystack)
        if query.lower() in haystack.lower():
            score += 0.35

        if score > best_score:
            best_score = score
            best = wine

    if best and best_score >= 0.28:
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
            str(den.get("notes", "")),
        ])

        score = similarity(query, haystack)
        if query.lower() in haystack.lower():
            score += 0.35

        if score > best_score:
            best_score = score
            best = den

    if best and best_score >= 0.28:
        best = dict(best)
        best["_score"] = round(best_score, 4)
        return best

    return None


def merge_profile(query, parsed, wine, denom, kb_matches):
    profile = {
        "query": query,
        "wine_title": None,
        "producer": None,
        "vintage": None,
        "country": None,
        "region": None,
        "denomination": None,
        "classification": None,
        "wine_type": None,
        "grape": None,
        "alcohol": None,
        "body": None,
        "acidity": None,
        "tannin": None,
        "oak": None,
        "aroma": None,
        "flavor": None,
        "soil": None,
        "climate": None,
        "allowed_grapes": None,
        "aging_rules": None,
        "notes": []
    }

    if parsed:
        profile["vintage"] = parsed.get("vintage")
        profile["grape"] = parsed.get("grape")
        if parsed.get("region"):
            profile["region"] = parsed.get("region")
        if parsed.get("denomination"):
            profile["denomination"] = parsed.get("denomination")
        if parsed.get("country"):
            profile["country"] = parsed.get("country")

    if wine:
        profile["wine_title"] = wine.get("wine_name")
        profile["producer"] = wine.get("producer")
        profile["vintage"] = wine.get("vintage") or profile["vintage"]
        profile["country"] = wine.get("country") or profile["country"]
        profile["region"] = wine.get("region") or profile["region"]
        profile["denomination"] = wine.get("denomination") or profile["denomination"]
        profile["wine_type"] = wine.get("wine_type") or profile["wine_type"]
        profile["grape"] = wine.get("grape") or profile["grape"]
        profile["alcohol"] = wine.get("alcohol") or profile["alcohol"]
        profile["body"] = wine.get("body") or profile["body"]
        profile["acidity"] = wine.get("acidity") or profile["acidity"]
        profile["tannin"] = wine.get("tannin") or profile["tannin"]
        profile["oak"] = wine.get("oak") or profile["oak"]
        profile["aroma"] = wine.get("aroma") or profile["aroma"]
        profile["flavor"] = wine.get("flavor") or profile["flavor"]
        profile["soil"] = wine.get("soil") or profile["soil"]
        profile["climate"] = wine.get("climate") or profile["climate"]
        profile["aging_rules"] = wine.get("aging_rules") or profile["aging_rules"]
        if wine.get("notes"):
            profile["notes"].append(f"Banco local vinho: {wine.get('notes')}")

    if denom:
        profile["country"] = denom.get("country") or profile["country"]
        profile["region"] = denom.get("region") or profile["region"]
        profile["denomination"] = denom.get("denomination") or profile["denomination"]
        profile["classification"] = denom.get("classification") or profile["classification"]
        profile["allowed_grapes"] = denom.get("allowed_grapes") or profile["allowed_grapes"]
        profile["soil"] = denom.get("soil") or profile["soil"]
        profile["climate"] = denom.get("climate") or profile["climate"]
        profile["aging_rules"] = denom.get("aging_rules") or profile["aging_rules"]
        if denom.get("min_alcohol") and not profile["alcohol"]:
            profile["alcohol"] = f"Mínimo legal da denominação: {denom.get('min_alcohol')}%"
        if denom.get("notes"):
            profile["notes"].append(f"Banco local denominação: {denom.get('notes')}")

    for item in kb_matches:
        data = item.get("data", {})
        profile["producer"] = data.get("producer") or profile["producer"]
        profile["wine_title"] = profile["wine_title"] or query
        profile["country"] = data.get("country") or profile["country"]
        profile["region"] = data.get("region") or profile["region"]
        profile["denomination"] = data.get("denomination") or profile["denomination"]
        profile["classification"] = data.get("classification") or profile["classification"]
        profile["wine_type"] = data.get("wine_type") or profile["wine_type"]
        profile["grape"] = data.get("grape") or profile["grape"]
        profile["alcohol"] = data.get("alcohol") or profile["alcohol"]
        profile["body"] = data.get("body") or profile["body"]
        profile["acidity"] = data.get("acidity") or profile["acidity"]
        profile["tannin"] = data.get("tannin") or profile["tannin"]
        profile["oak"] = data.get("oak") or profile["oak"]
        profile["aroma"] = data.get("aroma") or profile["aroma"]
        profile["flavor"] = data.get("flavor") or profile["flavor"]
        profile["soil"] = data.get("soil") or profile["soil"]
        profile["climate"] = data.get("climate") or profile["climate"]
        profile["aging_rules"] = data.get("aging_rules") or profile["aging_rules"]
        if data.get("grapes") and not profile["allowed_grapes"]:
            profile["allowed_grapes"] = data.get("grapes")
        if data.get("notes"):
            profile["notes"].append(f"Knowledge base: {data.get('notes')}")

    return profile


def build_wine_report(query: str):
    query = (query or "").strip()
    parsed = parse_wine_query(query) if query else {}
    wine = search_local_wine(query) if query else None
    denom = search_local_denomination(query) if query else None
    kb_matches = get_knowledge_matches(query, parsed) if query else []

    wine_web = search_wine_online(query) if query else []
    denom_web = search_denomination_online(query) if query else []

    profile = merge_profile(query, parsed, wine, denom, kb_matches)

    summary = []
    if wine:
        summary.append(f"Vinho encontrado no banco local: {wine.get('producer', '')} {wine.get('wine_name', '')}")
    if denom:
        summary.append(f"Denominação encontrada no banco local: {denom.get('denomination', '')}")
    if kb_matches:
        summary.append(f"Knowledge base encontrou {len(kb_matches)} correspondência(s).")
    if wine_web:
        summary.append(f"Busca web vinho/rótulo: {len(wine_web)} resultado(s).")
    if denom_web:
        summary.append(f"Busca web região/denominação: {len(denom_web)} resultado(s).")
    if not summary:
        summary.append("Sem correspondência local forte; resposta baseada em parser e busca web.")

    return {
        "query": query,
        "parsed_query": parsed,
        "wine_found": wine,
        "denomination_found": denom,
        "knowledge_matches": kb_matches,
        "profile": profile,
        "web": {
            "wine_results": wine_web,
            "denomination_results": denom_web
        },
        "summary": summary
    }
