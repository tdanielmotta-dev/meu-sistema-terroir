from difflib import SequenceMatcher

from database import fetch_all_wines, fetch_all_denominations
from parser_engine import parse_wine_query
from knowledge_base import get_knowledge_matches
from web_fetch import search_wine_online, search_denomination_online


# ---------------------------------------
# BUSCA LOCAL
# ---------------------------------------

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


# ---------------------------------------
# CONSOLIDAÇÃO
# ---------------------------------------

PROFILE_KEYS = [
    "wine_title", "producer", "vintage", "country", "region",
    "denomination", "classification", "wine_type", "grape",
    "alcohol", "body", "acidity", "tannin", "oak",
    "aroma", "flavor", "soil", "climate", "allowed_grapes",
    "aging_rules"
]


def empty_profile(query: str):
    return {
        "query": query,
        "wine_title": query,
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
        "notes": [],
        "sources_used": []
    }


def apply_if_empty(profile: dict, key: str, value, source_label: str = None):
    if value in (None, "", []):
        return
    if profile.get(key) in (None, "", []):
        profile[key] = value
        if source_label:
            profile["sources_used"].append(f"{key} ← {source_label}")


def merge_parsed(profile: dict, parsed: dict):
    if not parsed:
        return

    apply_if_empty(profile, "vintage", parsed.get("vintage"), "parser")
    apply_if_empty(profile, "grape", parsed.get("grape"), "parser")
    apply_if_empty(profile, "country", parsed.get("country"), "parser")
    apply_if_empty(profile, "region", parsed.get("region"), "parser")
    apply_if_empty(profile, "denomination", parsed.get("denomination"), "parser")


def merge_local_wine(profile: dict, wine: dict):
    if not wine:
        return

    mapping = {
        "wine_title": wine.get("wine_name"),
        "producer": wine.get("producer"),
        "vintage": wine.get("vintage"),
        "country": wine.get("country"),
        "region": wine.get("region"),
        "denomination": wine.get("denomination"),
        "wine_type": wine.get("wine_type"),
        "grape": wine.get("grape"),
        "alcohol": wine.get("alcohol"),
        "body": wine.get("body"),
        "acidity": wine.get("acidity"),
        "tannin": wine.get("tannin"),
        "oak": wine.get("oak"),
        "aroma": wine.get("aroma"),
        "flavor": wine.get("flavor"),
        "soil": wine.get("soil"),
        "climate": wine.get("climate"),
        "aging_rules": wine.get("aging_rules"),
    }

    for k, v in mapping.items():
        apply_if_empty(profile, k, v, "banco local vinho")

    if wine.get("notes"):
        profile["notes"].append(f"Banco local vinho: {wine.get('notes')}")


def merge_local_denom(profile: dict, denom: dict):
    if not denom:
        return

    mapping = {
        "country": denom.get("country"),
        "region": denom.get("region"),
        "denomination": denom.get("denomination"),
        "classification": denom.get("classification"),
        "allowed_grapes": denom.get("allowed_grapes"),
        "soil": denom.get("soil"),
        "climate": denom.get("climate"),
        "aging_rules": denom.get("aging_rules"),
    }

    for k, v in mapping.items():
        apply_if_empty(profile, k, v, "banco local denominação")

    if denom.get("min_alcohol") and not profile.get("alcohol"):
        profile["alcohol"] = f"Mínimo legal da denominação: {denom.get('min_alcohol')}%"
        profile["sources_used"].append("alcohol ← banco local denominação")

    if denom.get("notes"):
        profile["notes"].append(f"Banco local denominação: {denom.get('notes')}")


def merge_kb(profile: dict, kb_matches: list):
    for item in kb_matches or []:
        data = item.get("data", {})
        source = f"knowledge_base:{item.get('key')}"

        mapping = {
            "producer": data.get("producer"),
            "country": data.get("country"),
            "region": data.get("region"),
            "denomination": data.get("denomination"),
            "classification": data.get("classification"),
            "wine_type": data.get("wine_type"),
            "grape": data.get("grape"),
            "alcohol": data.get("alcohol"),
            "body": data.get("body"),
            "acidity": data.get("acidity"),
            "tannin": data.get("tannin"),
            "oak": data.get("oak"),
            "aroma": data.get("aroma"),
            "flavor": data.get("flavor"),
            "soil": data.get("soil"),
            "climate": data.get("climate"),
            "aging_rules": data.get("aging_rules"),
        }

        for k, v in mapping.items():
            apply_if_empty(profile, k, v, source)

        if data.get("grapes"):
            apply_if_empty(profile, "allowed_grapes", data.get("grapes"), source)

        if data.get("notes"):
            profile["notes"].append(f"Knowledge base: {data.get('notes')}")


def merge_web_pages(profile: dict, pages: list, source_prefix: str):
    """
    Regra: a internet agora preenche a ficha.
    Cada página traz item["extracted"] com campos estruturados.
    """
    for idx, page in enumerate(pages or [], start=1):
        extracted = page.get("extracted", {})
        if not extracted:
            continue

        src = f"{source_prefix}#{idx}"

        for key in [
            "producer", "vintage", "country", "region", "classification",
            "grape", "alcohol", "aroma", "flavor", "body", "acidity",
            "tannin", "oak", "soil", "climate", "aging_rules"
        ]:
            apply_if_empty(profile, key, extracted.get(key), src)

        title = page.get("title")
        url = page.get("url")
        if title or url:
            profile["notes"].append(f"Fonte web lida: {title or 'sem título'} | {url or ''}")


def build_summary(wine, denom, kb_matches, wine_web, denom_web, profile):
    summary = []

    if wine:
        summary.append(f"Vinho encontrado no banco local: {wine.get('producer', '')} {wine.get('wine_name', '')}")

    if denom:
        summary.append(f"Denominação encontrada no banco local: {denom.get('denomination', '')}")

    if kb_matches:
        summary.append(f"Knowledge base encontrou {len(kb_matches)} correspondência(s).")

    if wine_web:
        summary.append(f"Internet: {len(wine_web)} página(s) de vinho/rótulo processadas.")

    if denom_web:
        summary.append(f"Internet: {len(denom_web)} página(s) de região/denominação processadas.")

    filled = [k for k in PROFILE_KEYS if profile.get(k) not in (None, "", [])]
    summary.append(f"Campos preenchidos na ficha: {len(filled)}/{len(PROFILE_KEYS)}.")

    if profile.get("sources_used"):
        summary.append(f"Total de atribuições de fonte: {len(profile['sources_used'])}.")

    return summary


# ---------------------------------------
# FUNÇÃO PRINCIPAL
# ---------------------------------------

def build_wine_report(query: str):
    query = (query or "").strip()

    parsed = parse_wine_query(query) if query else {}
    wine = search_local_wine(query) if query else None
    denom = search_local_denomination(query) if query else None
    kb_matches = get_knowledge_matches(query, parsed) if query else []

    # Internet real: busca + extrai campos
    wine_web = search_wine_online(query, max_pages=5) if query else []
    denom_query = query
    if parsed.get("region"):
        denom_query += f" {parsed.get('region')}"
    if parsed.get("denomination"):
        denom_query += f" {parsed.get('denomination')}"
    denom_web = search_denomination_online(denom_query, max_pages=5) if query else []

    profile = empty_profile(query)

    # Ordem de merge:
    # 1 parser
    # 2 banco local vinho
    # 3 banco local denominação
    # 4 knowledge base
    # 5 internet vinho
    # 6 internet denominação
    merge_parsed(profile, parsed)
    merge_local_wine(profile, wine)
    merge_local_denom(profile, denom)
    merge_kb(profile, kb_matches)
    merge_web_pages(profile, wine_web, "web_vinho")
    merge_web_pages(profile, denom_web, "web_regiao")

    summary = build_summary(wine, denom, kb_matches, wine_web, denom_web, profile)

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
