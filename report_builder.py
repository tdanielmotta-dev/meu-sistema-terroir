from local_search import search_local_wine, search_local_denomination
from parser_engine import parse_wine_query
from web_fetch import search_wine_online, search_denomination_online


def build_wine_report(query: str):
    query = (query or "").strip()

    parsed = parse_wine_query(query) if query else {}

    wine = search_local_wine(query) if query else None
    denomination = search_local_denomination(query) if query else None

    wine_web = search_wine_online(query) if query else []
    denomination_web = search_denomination_online(query) if query else []

    report = {
        "query": query,
        "parsed_query": parsed,
        "wine_found": wine,
        "denomination_found": denomination,
        "web": {
            "wine_results": wine_web,
            "denomination_results": denomination_web,
        },
        "summary": []
    }

    if wine:
        report["summary"].append(
            f"Vinho localizado no banco: {wine.get('producer', '')} {wine.get('wine_name', '')} ({wine.get('vintage', '')})"
        )
    else:
        report["summary"].append("Nenhum vinho correspondente foi localizado no banco local.")

    if denomination:
        report["summary"].append(
            f"Denominação localizada: {denomination.get('denomination', '')} - {denomination.get('classification', '')}"
        )
    else:
        report["summary"].append("Nenhuma denominação correspondente foi localizada no banco local.")

    if wine_web:
        report["summary"].append(f"Busca online de vinho retornou {len(wine_web)} resultado(s).")
    else:
        report["summary"].append("Busca online de vinho sem resultados úteis.")

    if denomination_web:
        report["summary"].append(f"Busca online de denominação retornou {len(denomination_web)} resultado(s).")
    else:
        report["summary"].append("Busca online de denominação sem resultados úteis.")

    return report
