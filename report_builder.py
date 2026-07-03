from parser_engine import parse_wine_query
from local_search import search_local_wine, search_local_denomination
from web_fetch import search_wine_online, search_denomination_online


def merge_sources(local, online):
    return {
        "local": local,
        "online": online
    }


def build_consolidated_card(parsed, wine_local, den_local):
    card = {
        "producer": None,
        "wine_name": None,
        "vintage": None,
        "country": None,
        "region": None,
        "denomination": None,
        "classification": None,
        "wine_type": None,
        "grapes": [],
        "quality_terms": parsed.get("quality_terms", []),
        "styles_detected": parsed.get("styles_detected", []),
        "confidence": parsed.get("confidence", {})
    }

    # prioridade: banco local > parser
    if wine_local:
        card["producer"] = wine_local.get("producer")
        card["wine_name"] = wine_local.get("wine_name")
        card["vintage"] = wine_local.get("vintage")
        card["country"] = wine_local.get("country")
        card["region"] = wine_local.get("region")
        card["denomination"] = wine_local.get("denomination")
        card["classification"] = wine_local.get("classification")
        card["wine_type"] = wine_local.get("wine_type")

        grapes = wine_local.get("grape")
        if grapes:
            card["grapes"] = [g.strip() for g in str(grapes).split(",") if g.strip()]

    if den_local:
        if not card["country"]:
            card["country"] = den_local.get("country")
        if not card["region"]:
            card["region"] = den_local.get("region")
        if not card["denomination"]:
            card["denomination"] = den_local.get("denomination")
        if not card["classification"]:
            card["classification"] = den_local.get("classification")
        if not card["grapes"]:
            grapes = den_local.get("allowed_grapes")
            if grapes:
                card["grapes"] = [g.strip() for g in str(grapes).split(",") if g.strip()]

    if not card["producer"]:
        card["producer"] = parsed.get("producer_guess")
    if not card["wine_name"]:
        card["wine_name"] = parsed.get("wine_name_guess")
    if not card["vintage"]:
        card["vintage"] = parsed.get("year")
    if not card["country"]:
        card["country"] = parsed.get("country_guess")
    if not card["region"] and parsed.get("regions_detected"):
        card["region"] = parsed["regions_detected"][0]

    if not card["grapes"] and parsed.get("grapes_detected"):
        card["grapes"] = parsed.get("grapes_detected", [])

    if not card["classification"] and parsed.get("classifications"):
        card["classification"] = ", ".join(parsed.get("classifications", []))

    return card


def build_wine_report(query: str):
    query = (query or "").strip()

    parsed = parse_wine_query(query)

    wine_local = search_local_wine(query)
    den_local = search_local_denomination(query)

    wine_web = search_wine_online(query)
    den_web = search_denomination_online(query)

    consolidated = build_consolidated_card(parsed, wine_local, den_local)

    report = {
        "query": query,
        "parsed": parsed,
        "wine": merge_sources(wine_local, wine_web),
        "denomination": merge_sources(den_local, den_web),
        "consolidated": consolidated,
        "summary": []
    }

    # RESUMO DO PARSER
    if parsed.get("producer_guess"):
        report["summary"].append(f"Produtor provável: {parsed['producer_guess']}")
    if parsed.get("wine_name_guess"):
        report["summary"].append(f"Nome provável do vinho: {parsed['wine_name_guess']}")
    if parsed.get("year"):
        report["summary"].append(f"Safra detectada: {parsed['year']}")
    if parsed.get("country_guess"):
        report["summary"].append(f"País provável: {parsed['country_guess']}")
    if parsed.get("regions_detected"):
        report["summary"].append("Regiões detectadas: " + ", ".join(parsed["regions_detected"]))
    if parsed.get("classifications"):
        report["summary"].append("Classificações detectadas: " + ", ".join(parsed["classifications"]))
    if parsed.get("quality_terms"):
        report["summary"].append("Termos de qualidade detectados: " + ", ".join(parsed["quality_terms"]))
    if parsed.get("grapes_detected"):
        report["summary"].append("Uvas detectadas: " + ", ".join(parsed["grapes_detected"]))
    if parsed.get("styles_detected"):
        report["summary"].append("Estilos prováveis: " + ", ".join(parsed["styles_detected"]))

    # RESUMO LOCAL
    if wine_local:
        report["summary"].append(
            f"[LOCAL] Vinho encontrado: {wine_local.get('producer')} - {wine_local.get('wine_name')} ({wine_local.get('vintage')})"
        )
    else:
        report["summary"].append("[LOCAL] Nenhum vinho correspondente localizado no banco.")

    if den_local:
        report["summary"].append(
            f"[LOCAL] Denominação encontrada: {den_local.get('denomination')} ({den_local.get('classification')})"
        )
    else:
        report["summary"].append("[LOCAL] Nenhuma denominação correspondente localizada no banco.")

    # RESUMO WEB
    if wine_web:
        report["summary"].append(f"[WEB] {len(wine_web)} resultado(s) online para vinho/produtor/rótulo.")
    else:
        report["summary"].append("[WEB] Nenhum resultado online relevante para vinho/produtor/rótulo.")

    if den_web:
        report["summary"].append(f"[WEB] {len(den_web)} resultado(s) online para denominação/terroir/legislação.")
    else:
        report["summary"].append("[WEB] Nenhum resultado online relevante para denominação/terroir/legislação.")

    return report
