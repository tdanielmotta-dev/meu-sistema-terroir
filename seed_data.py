# Cada linha tem 12 campos:
# uid, country, macro_region, sub_region, appellation_name,
# legal_level, wine_color_scope, alcohol_min, alcohol_max,
# vintage_max, allowed_grapes, notes

SEED_ROWS = [
    # =====================================================
    # BORDEAUX
    # =====================================================
    (
        "FR-BOR-GRV",
        "França",
        "Bordeaux",
        "Graves",
        "Graves AOC",
        "AOC",
        "Tinto/Branco",
        10.5,
        None,
        2026,
        "Merlot;Cabernet Sauvignon;Cabernet Franc;Sémillon;Sauvignon Blanc;Muscadelle",
        "Bordeaux / Graves — seed base."
    ),
    (
        "FR-BOR-STN",
        "França",
        "Bordeaux",
        "Sauternes",
        "Sauternes AOC",
        "AOC",
        "Branco doce botrytizado",
        11.0,
        None,
        2026,
        "Sémillon;Sauvignon Blanc;Muscadelle",
        "Bordeaux / Sauternes — seed base."
    ),
    (
        "FR-BOR-BSC",
        "França",
        "Bordeaux",
        "Barsac",
        "Barsac AOC",
        "AOC",
        "Branco doce botrytizado",
        11.0,
        None,
        2026,
        "Sémillon;Sauvignon Blanc;Muscadelle",
        "Bordeaux / Barsac — seed base."
    ),
    (
        "FR-BOR-MED",
        "França",
        "Bordeaux",
        "Médoc",
        "Médoc AOC",
        "AOC",
        "Tinto",
        10.5,
        None,
        2026,
        "Cabernet Sauvignon;Merlot;Cabernet Franc;Petit Verdot;Malbec;Carménère",
        "Bordeaux / Médoc — seed base."
    ),

    # =====================================================
    # PIEMONTE
    # =====================================================
    (
        "IT-PIE-BAR",
        "Itália",
        "Piemonte",
        "Barolo",
        "Barolo DOCG",
        "DOCG",
        "Tinto",
        13.0,
        None,
        2026,
        "Nebbiolo",
        "Piemonte / Barolo — seed base."
    ),
    (
        "IT-PIE-BRB",
        "Itália",
        "Piemonte",
        "Barbaresco",
        "Barbaresco DOCG",
        "DOCG",
        "Tinto",
        12.5,
        None,
        2026,
        "Nebbiolo",
        "Piemonte / Barbaresco — seed base."
    ),
    (
        "IT-PIE-ROE",
        "Itália",
        "Piemonte",
        "Roero",
        "Roero DOCG",
        "DOCG",
        "Tinto/Branco",
        11.5,
        None,
        2026,
        "Nebbiolo;Arneis",
        "Piemonte / Roero — seed base."
    ),

    # =====================================================
    # RIOJA
    # =====================================================
    (
        "ES-RIO-ALT",
        "Espanha",
        "Rioja",
        "Rioja Alta",
        "Rioja DOCa",
        "DOCa",
        "Tinto/Branco/Rosado",
        11.0,
        None,
        2026,
        "Tempranillo;Garnacha;Graciano;Mazuelo;Viura;Malvasía;Garnacha Blanca",
        "Rioja Alta — seed base."
    ),
    (
        "ES-RIO-ALA",
        "Espanha",
        "Rioja",
        "Rioja Alavesa",
        "Rioja DOCa",
        "DOCa",
        "Tinto/Branco/Rosado",
        11.0,
        None,
        2026,
        "Tempranillo;Garnacha;Graciano;Mazuelo;Viura;Malvasía;Garnacha Blanca",
        "Rioja Alavesa — seed base."
    ),
    (
        "ES-RIO-ORB",
        "Espanha",
        "Rioja",
        "Rioja Oriental",
        "Rioja DOCa",
        "DOCa",
        "Tinto/Branco/Rosado",
        11.0,
        None,
        2026,
        "Tempranillo;Garnacha;Graciano;Mazuelo;Viura;Malvasía;Garnacha Blanca",
        "Rioja Oriental — seed base."
    ),

    # =====================================================
    # PORTUGAL
    # =====================================================
    (
        "PT-DOR-CCG",
        "Portugal",
        "Douro",
        "Cima Corgo",
        "Douro DOC",
        "DOC",
        "Tinto/Branco/Fortificado",
        11.0,
        None,
        2026,
        "Touriga Nacional;Touriga Franca;Tinta Roriz;Tinto Cão;Rabigato;Viosinho;Gouveio",
        "Douro / Cima Corgo — seed base."
    ),

    # =====================================================
    # BRASIL
    # =====================================================
    (
        "BR-MG-MAN",
        "Brasil",
        "Minas Gerais",
        "Mantiqueira",
        "Mantiqueira de Minas",
        "IG/DO",
        "Tinto/Branco/Espumante",
        10.0,
        None,
        2026,
        "Syrah;Sauvignon Blanc;Chardonnay;Pinot Noir",
        "Mantiqueira de Minas — seed base."
    )
]
