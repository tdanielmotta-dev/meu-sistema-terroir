from local_search import search_local_wine, search_local_denomination
from web_fetch import search_wine_online, search_denomination_online


def merge_sources(local, online):
    return {
        "local": local,
        "online": online
    }


def build_wine_report(query: str):
    query = (query or "").strip()

    # =========================
    # 1. LOCAL SEARCH
    # =========================
    wine_local = search_local_wine(query)
    den_local = search_local_denomination(query)

    # =========================
    # 2. WEB SEARCH
    # =========================
    wine_web = search_wine_online(query)
    den_web = search_denomination_online(query)

    # =========================
    # 3. REPORT STRUCTURE
    # =========================
    report = {
        "query": query,
        "wine": merge_sources(wine_local, wine_web),
        "denomination": merge_sources(den_local, den_web),
        "summary": []
    }

    # =========================
    # 4. SUMMARY LOGIC
    # =========================
    if wine_local:
        report["summary"].append(
            f"[LOCAL] Vinho encontrado: {wine_local.get('producer')} - {wine_local.get('wine_name')}"
        )
    else:
        report["summary"].append("[LOCAL] Nenhum vinho encontrado no banco local.")

    if wine_web:
        report["summary"].append(f"[WEB] {len(wine_web)} fontes online encontradas para o vinho.")

    if den_local:
        report["summary"].append(
            f"[LOCAL] Denominação: {den_local.get('denomination')} ({den_local.get('classification')})"
        )
    else:
        report["summary"].append("[LOCAL] Nenhuma denominação encontrada no banco.")

    if den_web:
        report["summary"].append(f"[WEB] {len(den_web)} fontes online para denominação.")

    return report
