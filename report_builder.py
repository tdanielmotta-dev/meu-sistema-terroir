from parser_engine import parse_label_text
from local_search import search_local_wine, search_local_denomination
from web_fetch import search_wine_online, search_denomination_online
from knowledge_base import infer_from_query


def build_wine_report(query: str):
    parsed = parse_label_text(query)

    local_wine = search_local_wine(query)
    local_denomination = search_local_denomination(query)

    # enriquecimento por parser
    enriched_query_parts = [query]

    if parsed.get("denominations_detected"):
        enriched_query_parts.extend(parsed["denominations_detected"])

    if parsed.get("grapes_detected"):
        enriched_query_parts.extend(parsed["grapes_detected"])

    enriched_query = " ".join(dict.fromkeys(enriched_query_parts))

    online_wine = search_wine_online(enriched_query)
    online_denomination = search_denomination_online(enriched_query)

    kb_matches = infer_from_query(enriched_query)

    summary = []

    if local_wine:
        summary.append(
            f"Vinho localizado no banco local: {local_wine.get('producer', '')} "
            f"{local_wine.get('wine_name', '')} ({local_wine.get('vintage', '')})."
        )
    else:
        summary.append("Nenhum vinho exato foi localizado no banco local.")

    if local_denomination:
        summary.append(
            f"Denominação localizada no banco local: {local_denomination.get('denomination', '')} "
            f"({local_denomination.get('classification', '')})."
        )
    else:
        summary.append("Nenhuma denominação exata foi localizada no banco local.")

    if kb_matches:
        summary.append(
            f"Knowledge base identificou {len(kb_matches)} denominação(ões)/região(ões) compatível(is) com o texto do rótulo."
        )
    else:
        summary.append("Knowledge base não encontrou uma denominação fortemente reconhecida no texto.")

    if online_wine:
        summary.append(f"Foram encontrados {len(online_wine)} resultados online relacionados ao vinho/rótulo.")
    else:
        summary.append("Nenhum resultado online relevante do vinho foi encontrado nesta rodada.")

    if online_denomination:
        summary.append(f"Foram encontrados {len(online_denomination)} resultados online sobre denominação/região.")
    else:
        summary.append("Nenhum resultado online relevante de denominação foi encontrado nesta rodada.")

    return {
        "query": query,
        "parsed": parsed,
        "wine_found": local_wine,
        "denomination_found": local_denomination,
        "knowledge_matches": kb_matches,
        "online_wine_results": online_wine,
        "online_denomination_results": online_denomination,
        "summary": summary
    }
