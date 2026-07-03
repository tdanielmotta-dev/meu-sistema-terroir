import re

KNOWN_GRAPES = [
    "cabernet sauvignon", "merlot", "pinot noir", "chardonnay", "syrah",
    "shiraz", "malbec", "nebbiolo", "sangiovese", "tempranillo",
    "sauvignon blanc", "semillon", "muscadelle", "riesling",
    "gewurztraminer", "grenache", "garnacha", "touriga nacional",
    "cabernet franc", "carmenere", "zinfandel", "primitivo", "barbera"
]

KNOWN_DENOMINATIONS = [
    "barolo", "barbaresco", "bordeaux", "medoc", "haut-medoc",
    "pauillac", "margaux", "saint-estephe", "saint-julien",
    "pomerol", "saint-emilion", "sauternes", "barsac", "graves",
    "rioja", "chianti", "chianti classico", "brunello di montalcino",
    "amarone", "valpolicella", "bourgogne", "chablis", "champagne"
]

KNOWN_COUNTRIES = [
    "frança", "france", "itália", "italy", "espanha", "spain",
    "portugal", "argentina", "chile", "brasil", "austrália", "australia",
    "eua", "usa", "estados unidos", "alemanha", "germany"
]

STYLE_TERMS = [
    "reserva", "gran reserva", "classico", "superiore", "riserva",
    "brut", "extra brut", "demi-sec", "sec", "doce", "botrytized",
    "late harvest", "icewine", "rosso", "bianco", "blanc", "rouge"
]


def normalize(text: str) -> str:
    return (text or "").strip().lower()


def parse_label_text(label_text: str):
    text = normalize(label_text)

    vintage = None
    vintages = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    if vintages:
        vintage = vintages[0]

    grapes = []
    for g in KNOWN_GRAPES:
        if g in text:
            grapes.append(g.title())

    denominations = []
    for d in KNOWN_DENOMINATIONS:
        if d in text:
            denominations.append(d.title())

    countries = []
    for c in KNOWN_COUNTRIES:
        if c in text:
            countries.append(c.title())

    styles = []
    for s in STYLE_TERMS:
        if s in text:
            styles.append(s.title())

    tokens = [t for t in re.split(r"[^a-zA-ZÀ-ÿ0-9]+", label_text) if t.strip()]
    probable_name = " ".join(tokens[:8]).strip()

    return {
        "raw_label": label_text,
        "probable_name": probable_name,
        "vintage": vintage,
        "grapes_detected": grapes,
        "denominations_detected": denominations,
        "countries_detected": countries,
        "style_terms": styles
    }
