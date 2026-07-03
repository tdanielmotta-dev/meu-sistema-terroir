from parser_engine import parse_wine_query
from local_search import search_local_wine, search_local_denomination
from web_search import search_wine_online, search_denomination_online
from extractors import extract_profile_from_text
from database import save_online_result_to_db


def merge_value(base, incoming):
    if incoming in [None, "", [], {}]:
        return base
    if base in [None, "", [], {}]:
        return incoming

    # se ambos são listas, junta sem duplicar
    if isinstance(base, list) and isinstance(incoming, list):
        out = list(base)
        seen = {str(x).lower() for x in out}
        for item in incoming:
            if str(item).lower() not in seen:
                out.append(item)
                seen.add(str(item).lower())
        return out

    # mantém o que já existe
    return base


def merge_profiles(*profiles):
    final = {
        "producer": None,
        "wine_name": None,
        "vintage": None,
        "grape": None,
        "other_grapes": [],
        "country": None,
        "region": None,
        "subregion": None,
        "denomination": None,
        "classification": None,
        "wine_type": None,
        "alcohol": None,
        "climate": None,
        "soil": None,
        "terroir": None,
        "acidity": None,
        "body": None,
        "tannins": None,
        "aging": None,
        "aromas": None,
        "palate": None,
        "pairing": None,
        "notes": None,
    }

    for profile in profiles:
        if not profile:
            continue
        for key in final.keys():
            final[key] = merge_value(final.get(key), profile.get(key))

    return final


def wine_to_profile(wine: dict):
    if not wine:
        return {}
    return {
        "producer": wine.get("producer"),
        "wine_name": wine.get("wine_name"),
        "vintage": wine.get("vintage"),
        "grape": wine.get("grape"),
        "country": wine.get("country"),
        "region": wine.get("region"),
        "subregion": wine.get("subregion"),
        "denomination": wine.get("denomination"),
        "classification": wine.get("classification"),
        "wine_type": wine.get("wine_type"),
        "alcohol": f"{wine.get('alcohol')}%" if wine.get("alcohol") not in [None, ""] else None,
        "climate": wine.get("climate"),
        "soil": wine.get("soil"),
        "terroir": wine.get("terroir"),
        "acidity": wine.get("acidity"),
        "body": wine.get("body"),
        "tannins": wine.get("tannins"),
        "aging": wine.get("aging"),
        "aromas": wine.get("aromas"),
        "palate": wine.get("palate"),
        "pairing": wine.get("pairing"),
        "notes": wine.get("notes"),
        "other_grapes": []
    }


def denom_to_profile(den: dict):
    if not den:
        return {}
    grapes = []
    raw = den.get("allowed_grapes")
    if raw:
        grapes = [x.strip() for x in str(raw).split(",") if x.strip()]

    return {
        "country": den.get("country"),
        "region": den.get("region"),
        "subregion": den.get("subregion"),
        "denomination": den.get("denomination"),
        "classification": den.get("classification"),
        "grape": grapes[0] if grapes else None,
        "other_grapes": grapes[1:] if len(grapes) > 1 else [],
        "alcohol": f"{den.get('min_alcohol')}% mínimo" if den.get("min_alcohol") not in [None, ""] else None,
        "aging": den.get("aging_rules"),
        "climate": den.get("climate"),
        "soil": den.get("soil"),
        "terroir": den.get("terroir"),
        "notes": den.get("notes"),
    }


def parsed_to_profile(parsed: dict):
    if not parsed:
        return {}
    grapes = parsed.get("grapes_found") or []
    return {
        "producer": parsed.get("producer_guess"),
        "wine_name": parsed.get("wine_name_guess"),
        "vintage": parsed.get("vintage"),
        "grape": grapes[0] if grapes else None,
        "other_grapes": grapes[1:] if len(grapes) > 1 else [],
        "classification": parsed.get("denom_terms_found", [None])[0] if parsed.get("denom_terms_found") else None
    }


def build_wine_report(query: str):
    parsed = parse_wine_query(query)

    local_wine = search_local_wine(query)
    local_denom = search_local_denomination(query)

    wine_results = search_wine_online(query)
    denom_results = search_denomination_online(query)

    all_sources = []
    seen_urls = set()

    for item in wine_results + denom_results:
        url = item.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            all_sources.append(item)

    extracted_profiles = []
    online_sources = []

    for item in all_sources:
        extracted = extract_profile_from_text(
            query=query,
            title=item.get("title", ""),
            snippet=item.get("snippet", ""),
            page_summary=item.get("page_summary", "")
        )
        enriched = dict(item)
        enriched["extracted"] = extracted
        online_sources.append(enriched)
        if extracted:
            extracted_profiles.append(extracted)

    final_profile = merge_profiles(
        parsed_to_profile(parsed),
        wine_to_profile(local_wine),
        denom_to_profile(local_denom),
        *extracted_profiles
    )

    summary = []

    summary.append(f"Consulta: {query}")

    if local_wine:
        summary.append(
            f"Vinho localizado no banco local: {local_wine.get('producer', '')} {local_wine.get('wine_name', '')} "
            f"({local_wine.get('vintage', '')})"
        )
    else:
        summary.append("Nenhum vinho correspondente foi localizado no banco local.")

    if local_denom:
        summary.append(
            f"Denominação localizada no banco: {local_denom.get('denomination', '')} "
            f"- {local_denom.get('classification', '')}"
        )
    else:
        summary.append("Nenhuma denominação correspondente foi localizada no banco local.")

    if online_sources:
        summary.append(f"Foram consolidadas {len(online_sources)} fontes online.")
    else:
        summary.append("Nenhuma fonte online útil foi consolidada.")

    # salva resultado consolidado no banco para enriquecer pesquisas futuras
    try:
        save_online_result_to_db(final_profile)
        summary.append("Resultado consolidado salvo no banco local para reaproveitamento futuro.")
    except Exception:
        summary.append("Falha ao salvar o resultado consolidado no banco local.")

    return {
        "query": query,
        "parsed_query": parsed,
        "wine_found": local_wine,
        "denomination_found": local_denom,
        "online_sources": online_sources,
        "final_profile": final_profile,
        "summary": summary
    }
