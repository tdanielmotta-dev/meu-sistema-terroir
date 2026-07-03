from local_search import search_local_wine, search_local_denomination


def build_wine_report(query: str):
    wine = search_local_wine(query)
    denomination = search_local_denomination(query)

    report = {
        "query": query,
        "wine_found": wine,
        "denomination_found": denomination,
        "summary": []
    }

    if wine:
        report["summary"].append(
            f"Vinho localizado no banco: {wine.get('producer', '')} {wine.get('wine_name', '')} "
            f"({wine.get('vintage', '')})"
        )
    else:
        report["summary"].append("Nenhum vinho correspondente foi localizado no banco local.")

    if denomination:
        report["summary"].append(
            f"Denominação localizada: {denomination.get('denomination', '')} "
            f"- {denomination.get('classification', '')}"
        )
    else:
        report["summary"].append("Nenhuma denominação correspondente foi localizada no banco local.")

    return report
