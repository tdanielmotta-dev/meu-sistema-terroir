from parser_engine import parse_query
from local_search import (
    search_local_wine,
    search_local_denomination,
    search_local_producer
)
from web_fetch import search_wine_online, search_denomination_online


def build_wine_report(query: str):
    query = (query or "").strip()

    parsed = parse_query(query)

    wine = search_local_wine(query)
    denomination = search_local_denomination(query)
    producer = search_local_producer(query)

    web_wine = search_wine_online(query)
    denom_query = (
        parsed.get("denomination_hint")
        or parsed.get("region_hint")
        or query
    )
    web_denom = search_denomination_online(denom_query)

    summary = []

    if wine:
        summary.append(
            f"Vinho localizado no banco local: {wine.get('producer', '')} {wine.get('wine_name', '')} "
            f"({wine.get('vintage', '')}) — score {wine.get('_score', '')}"
        )
    else:
        summary.append("Nenhum vinho correspondente foi localizado no banco local.")

    if denomination:
        summary.append(
            f"Denominação localizada no banco local: {denomination.get('denomination', '')} "
            f"({denomination.get('classification', '')}) — score {denomination.get('_score', '')}"
        )
    else:
        summary.append("Nenhuma denominação correspondente foi localizada no banco local.")

    if producer:
        summary.append(
            f"Produtor localizado no banco local: {producer.get('producer_name', '')} "
            f"— score {producer.get('_score', '')}"
        )
    else:
        summary.append("Nenhum produtor correspondente foi localizado no banco local.")

    if web_wine:
        summary.append(f"Busca online retornou {len(web_wine)} resultado(s) principais para o vinho/rótulo.")
    else:
        summary.append("Busca online do vinho/rótulo não retornou resultados úteis.")

    if web_denom:
        summary.append(f"Busca online retornou {len(web_denom)} resultado(s) principais para denominação/região.")
    else:
        summary.append("Busca online da denominação/região não retornou resultados úteis.")

    report = {
        "query": query,
        "parsed": parsed,
        "wine_found": wine,
        "denomination_found": denomination,
        "producer_found": producer,
        "web_wine_results": web_wine,
        "web_denom_results": web_denom,
        "summary": summary,
    }

    return report
