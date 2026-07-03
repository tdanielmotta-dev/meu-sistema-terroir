# =====================================================================================
# WINEINDEX OMEGA V10 — DEFINITIVE MASTER BUILD
# APP.PY — V1 + V2 + V3 INTEGRADOS
# =====================================================================================

import streamlit as st
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# =====================================================================================
# CONFIG GERAL
# =====================================================================================

st.set_page_config(
    page_title="WINEINDEX OMEGA V10",
    page_icon="🍷",
    layout="wide"
)

DB_NAME = "wineindex_omega.db"

# =====================================================================================
# TAXONOMIAS GLOBAIS
# =====================================================================================

SOIL_TAXONOMY = [
    "Calcário", "Xisto", "Granito", "Argila", "Areia", "Basalto",
    "Vulcânico", "Aluvial", "Cascalho", "Marga", "Gnaisse", "Ardósia"
]

CLIMATE_TAXONOMY = [
    "Oceânico", "Continental", "Mediterrâneo", "Alpino", "Semiárido",
    "Marítimo", "Subtropical", "Desértico", "Montanhoso"
]

STYLE_TAXONOMY = [
    "Alta acidez", "Corpo leve", "Corpo médio", "Corpo alto",
    "Tanino baixo", "Tanino médio", "Tanino elevado",
    "Mineralidade intensa", "Guarda longa", "Frutado intenso",
    "Barricado", "Espumante tradicional", "Doce botrytizado"
]

LEGAL_TYPES = [
    "AOC", "AOP", "DOC", "DOCG", "DOP", "DO", "DOCa", "IGP", "IGT",
    "AVA", "GI", "IPR", "Vinho Regional", "Indicação Geográfica", "Outro"
]

WINE_STYLES = [
    "Tinto", "Branco", "Rosé", "Espumante", "Fortificado",
    "Doce", "Botrytizado", "Natural", "Laranja", "Vegano"
]

LAYER_CODES = [
    "GEO", "LEG", "TER", "UVA", "TEC", "SEN", "HIST", "COM"
]

# =====================================================================================
# HELPERS
# =====================================================================================

def to_json(value):
    if value is None:
        return json.dumps([])
    if isinstance(value, str):
        return json.dumps([value], ensure_ascii=False)
    return json.dumps(value, ensure_ascii=False)

def from_json(value):
    if not value:
        return []
    try:
        return json.loads(value)
    except:
        return []

def safe_float(v, default=0.0):
    try:
        return float(v)
    except:
        return default

def generate_universal_id(country: str, macro_region: str, sub_region: str) -> str:
    c = (country or "XX")[:2].upper()
    m = (macro_region or "XXX")[:3].upper().replace(" ", "_")
    s = (sub_region or "XXX")[:3].upper().replace(" ", "_")
    return f"{c}-{m}-{s}"

def badge(text, color="#5a3d2b"):
    st.markdown(
        f"""
        <span style="
            background:{color};
            color:white;
            padding:4px 10px;
            border-radius:999px;
            font-size:0.85rem;
            margin-right:6px;
            display:inline-block;
            margin-bottom:6px;
        ">{text}</span>
        """,
        unsafe_allow_html=True
    )

# =====================================================================================
# BANCO DE DADOS
# =====================================================================================

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # -----------------------------
    # Tabela principal de denominações
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS denominations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        universal_id TEXT UNIQUE,

        name TEXT NOT NULL,
        country TEXT,
        macro_region TEXT,
        sub_region TEXT,
        legal_classification TEXT,
        denomination_type TEXT,

        latitude REAL,
        longitude REAL,
        altitude_avg REAL,
        topography TEXT,
        ocean_proximity TEXT,
        continental_influence TEXT,
        rivers TEXT,

        soils TEXT,
        climate_classification TEXT,
        thermal_amplitude TEXT,
        precipitation TEXT,
        sunshine TEXT,
        climate_risks TEXT,
        natural_influences TEXT,

        legislation_rules TEXT,
        max_yield TEXT,
        min_alcohol REAL,
        aging_requirements TEXT,
        authorized_methods TEXT,
        restrictions TEXT,

        grapes_json TEXT,
        production_json TEXT,
        sensory_json TEXT,
        wine_styles_json TEXT,
        subregions_json TEXT,
        cities_json TEXT,
        micro_terroirs_json TEXT,

        history TEXT,
        particularities TEXT,
        technical_comparisons TEXT,
        official_references TEXT,

        geo_layer TEXT,
        leg_layer TEXT,
        ter_layer TEXT,
        uva_layer TEXT,
        tec_layer TEXT,
        sen_layer TEXT,
        hist_layer TEXT,
        com_layer TEXT,

        created_at TEXT,
        updated_at TEXT
    )
    """)

    # -----------------------------
    # Auditorias de rótulo
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS label_audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wine_name TEXT,
        denomination_name TEXT,
        vintage INTEGER,
        alcohol REAL,
        grape TEXT,
        country TEXT,
        result TEXT,
        errors_json TEXT,
        created_at TEXT
    )
    """)

    # -----------------------------
    # Estado do sistema
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS system_state (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()

# =====================================================================================
# SEED INICIAL
# =====================================================================================

def seed_if_empty():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM denominations")
    count = cur.fetchone()[0]

    if count == 0:
        seed_data = [
            {
                "name": "Sauternes",
                "country": "França",
                "macro_region": "Bordeaux",
                "sub_region": "Sauternais",
                "legal_classification": "AOC",
                "denomination_type": "Denominação de Origem",
                "latitude": 44.53,
                "longitude": -0.34,
                "altitude_avg": 30,
                "topography": "Ondulada suave, colinas baixas, vales drenantes",
                "ocean_proximity": "Influência atlântica indireta",
                "continental_influence": "Moderada",
                "rivers": "Garonne; Ciron",
                "soils": to_json(["Cascalho", "Argila", "Calcário", "Areia"]),
                "climate_classification": "Oceânico com microclima favorável à botrytis",
                "thermal_amplitude": "Moderada",
                "precipitation": "Moderada a alta",
                "sunshine": "Boa insolação em maturação",
                "climate_risks": "Podridões indesejadas, chuva na colheita",
                "natural_influences": "Nevoeiros do Ciron e Garonne, umidade matinal, secagem diurna",
                "legislation_rules": "Brancos doces botrytizados; colheita seletiva; foco em uvas sobremaduras afetadas por Botrytis cinerea.",
                "max_yield": "Conforme caderno de especificações AOC",
                "min_alcohol": 12.0,
                "aging_requirements": "Variável por produtor; estilo frequentemente apto a longa guarda",
                "authorized_methods": "Colheitas sucessivas por triagem, vinificação de mostos concentrados",
                "restrictions": "Uvas e área delimitada conforme AOC",
                "grapes_json": to_json([
                    {
                        "grape": "Sémillon",
                        "function": "Base estrutural e botrytis",
                        "percent_allowed": "Principal",
                        "sensory": "Mel, damasco, cera, volume",
                        "climatic_adaptation": "Excelente em botrytização"
                    },
                    {
                        "grape": "Sauvignon Blanc",
                        "function": "Acidez e frescor",
                        "percent_allowed": "Complementar",
                        "sensory": "Cítricos, ervas, tensão",
                        "climatic_adaptation": "Boa em clima oceânico"
                    },
                    {
                        "grape": "Muscadelle",
                        "function": "Aromática complementar",
                        "percent_allowed": "Secundária",
                        "sensory": "Floral, especiarias doces",
                        "climatic_adaptation": "Pontual"
                    }
                ]),
                "production_json": to_json({
                    "harvest": "Passagens sucessivas no vinhedo",
                    "pressing": "Prensagem delicada",
                    "fermentation": "Fermentação de mosto concentrado",
                    "wood_stage": "Frequentemente em carvalho",
                    "traditional_methods": "Triagem de bagos botrytizados",
                    "modern_techniques": "Controle térmico e higiene rigorosa"
                }),
                "sensory_json": to_json({
                    "primary_aromas": ["Damasco", "Pêssego", "Casca de laranja"],
                    "secondary_aromas": ["Mel", "Baunilha", "Pão doce"],
                    "tertiary_aromas": ["Cera", "Açafrão", "Frutos secos"],
                    "structure": "Untuoso, concentrado",
                    "acidity": "Média a alta",
                    "tannins": "N/A",
                    "finish": "Longuíssimo",
                    "aging_potential": "Muito alto"
                }),
                "wine_styles_json": to_json(["Branco", "Doce", "Botrytizado"]),
                "subregions_json": to_json(["Sauternes", "Barsac"]),
                "cities_json": to_json(["Sauternes", "Barsac", "Bommes", "Fargues"]),
                "micro_terroirs_json": to_json(["Encostas drenantes próximas ao Ciron", "Setores de cascalho e argila"]),
                "history": "Região clássica de vinhos doces botrytizados de Bordeaux.",
                "particularities": "Botrytis nobre é o núcleo identitário da região.",
                "technical_comparisons": "Comparable a Tokaji e Beerenauslese/TBA em lógica de concentração natural, mas com identidade bordalesa.",
                "official_references": "INAO; cahiers des charges da AOC",
            },
            {
                "name": "Barolo",
                "country": "Itália",
                "macro_region": "Piemonte",
                "sub_region": "Langhe",
                "legal_classification": "DOCG",
                "denomination_type": "Denominação de Origem",
                "latitude": 44.61,
                "longitude": 7.94,
                "altitude_avg": 300,
                "topography": "Colinas íngremes com exposições variadas",
                "ocean_proximity": "Baixa",
                "continental_influence": "Alta",
                "rivers": "Tanaro (influência regional)",
                "soils": to_json(["Marga", "Calcário", "Argila"]),
                "climate_classification": "Continental",
                "thermal_amplitude": "Alta",
                "precipitation": "Moderada",
                "sunshine": "Boa",
                "climate_risks": "Geadas, granizo, chuvas de fim de ciclo",
                "natural_influences": "Colinas, neblinas sazonais, diferenças de exposição",
                "legislation_rules": "Barolo DOCG; Nebbiolo como base exclusiva do estilo clássico da denominação.",
                "max_yield": "Conforme disciplinare DOCG",
                "min_alcohol": 13.0,
                "aging_requirements": "Envelhecimento mínimo regulamentado pela DOCG",
                "authorized_methods": "Vinificação tinta tradicional ou moderna dentro das regras DOCG",
                "restrictions": "Área delimitada, prazos mínimos, Nebbiolo",
                "grapes_json": to_json([
                    {
                        "grape": "Nebbiolo",
                        "function": "Casta principal absoluta",
                        "percent_allowed": "100%",
                        "sensory": "Rosas, alcatrão, cereja, tanino alto",
                        "climatic_adaptation": "Muito adaptada às colinas de Langhe"
                    }
                ]),
                "production_json": to_json({
                    "harvest": "Tardia",
                    "pressing": "Convencional para tintos",
                    "fermentation": "Macerada; pode variar por produtor",
                    "wood_stage": "Frequentemente em botti ou barrica",
                    "traditional_methods": "Macerações longas e botti",
                    "modern_techniques": "Macerações mais curtas e barricas menores"
                }),
                "sensory_json": to_json({
                    "primary_aromas": ["Cereja", "Rosa", "Framboesa ácida"],
                    "secondary_aromas": ["Especiarias", "Chá"],
                    "tertiary_aromas": ["Alcatrão", "Cogumelos", "Tabaco"],
                    "structure": "Muito estruturado",
                    "acidity": "Alta",
                    "tannins": "Altos",
                    "finish": "Longo",
                    "aging_potential": "Muito alto"
                }),
                "wine_styles_json": to_json(["Tinto"]),
                "subregions_json": to_json(["Barolo", "La Morra", "Monforte d'Alba", "Serralunga d'Alba", "Castiglione Falletto"]),
                "cities_json": to_json(["Barolo", "La Morra", "Monforte d'Alba", "Serralunga d'Alba"]),
                "micro_terroirs_json": to_json(["Cannubi", "Brunate", "Cerequio", "Rocche"]),
                "history": "Uma das grandes DOCGs italianas baseadas em Nebbiolo.",
                "particularities": "Confronto clássico entre estilos mais tradicionais e mais modernos.",
                "technical_comparisons": "Comparável a Barbaresco em uva, mas normalmente mais austero, potente e longevo.",
                "official_references": "Ministero dell'Agricoltura; Consorzio Barolo Barbaresco Alba Langhe e Dogliani",
            },
            {
                "name": "Rioja",
                "country": "Espanha",
                "macro_region": "La Rioja",
                "sub_region": "Rioja DOCa",
                "legal_classification": "DOCa",
                "denomination_type": "Denominação de Origem",
                "latitude": 42.46,
                "longitude": -2.45,
                "altitude_avg": 450,
                "topography": "Vale e encostas sob influência montanhosa",
                "ocean_proximity": "Indireta",
                "continental_influence": "Moderada a alta",
                "rivers": "Ebro",
                "soils": to_json(["Argila", "Calcário", "Aluvial", "Ferroso"]),
                "climate_classification": "Misto entre atlântico, continental e mediterrâneo",
                "thermal_amplitude": "Moderada",
                "precipitation": "Variável conforme subzona",
                "sunshine": "Boa",
                "climate_risks": "Seca, geadas localizadas, granizo",
                "natural_influences": "Serra Cantábrica, vale do Ebro",
                "legislation_rules": "DOCa com categorias e menções geográficas específicas; inclui Viñedos Singulares.",
                "max_yield": "Conforme regulamento DOCa Rioja",
                "min_alcohol": 12.0,
                "aging_requirements": "Dependem da categoria (joven, crianza, reserva, gran reserva etc.)",
                "authorized_methods": "Conforme regulamento do Consejo Regulador",
                "restrictions": "Castas, origem, rendimentos e menções geográficas controladas",
                "grapes_json": to_json([
                    {
                        "grape": "Tempranillo",
                        "function": "Base principal",
                        "percent_allowed": "Principal",
                        "sensory": "Fruta vermelha, especiarias, estrutura média",
                        "climatic_adaptation": "Excelente"
                    },
                    {
                        "grape": "Garnacha",
                        "function": "Complemento ou base em alguns vinhos",
                        "percent_allowed": "Permitida",
                        "sensory": "Fruta madura, calor, volume",
                        "climatic_adaptation": "Boa em zonas mais quentes"
                    },
                    {
                        "grape": "Graciano",
                        "function": "Acidez e estrutura aromática",
                        "percent_allowed": "Permitida",
                        "sensory": "Especiarias, acidez, longevidade",
                        "climatic_adaptation": "Boa"
                    }
                ]),
                "production_json": to_json({
                    "harvest": "Setembro a outubro, variável",
                    "pressing": "Conforme estilo",
                    "fermentation": "Aço, concreto ou madeira",
                    "wood_stage": "Muito frequente em estilos tradicionais",
                    "traditional_methods": "Longo uso de carvalho",
                    "modern_techniques": "Precisão parcelar, menor extração, foco de terroir"
                }),
                "sensory_json": to_json({
                    "primary_aromas": ["Cereja", "Ameixa", "Framboesa"],
                    "secondary_aromas": ["Baunilha", "Coco", "Especiarias"],
                    "tertiary_aromas": ["Tabaco", "Couro", "Folha seca"],
                    "structure": "Média a alta",
                    "acidity": "Média a alta",
                    "tannins": "Médios",
                    "finish": "Médio a longo",
                    "aging_potential": "Médio a alto"
                }),
                "wine_styles_json": to_json(["Tinto", "Branco", "Rosé"]),
                "subregions_json": to_json(["Rioja Alta", "Rioja Alavesa", "Rioja Oriental"]),
                "cities_json": to_json(["Haro", "Logroño", "Laguardia"]),
                "micro_terroirs_json": to_json(["Viñedos Singulares", "Parcelas históricas"]),
                "history": "Uma das grandes denominações espanholas, referência em envelhecimento e hoje também em terroir parcelar.",
                "particularities": "Convivem escolas tradicionais e modernas; Viñedos Singulares adicionam camada parcelar relevante.",
                "technical_comparisons": "Pode cruzar lógica de classificação por envelhecimento com nova lógica de origem parcelar.",
                "official_references": "Consejo Regulador DOCa Rioja",
            }
        ]

        now = datetime.now().isoformat()

        for d in seed_data:
            universal_id = generate_universal_id(
                d["country"], d["macro_region"], d["sub_region"]
            )

            cur.execute("""
            INSERT OR IGNORE INTO denominations (
                universal_id, name, country, macro_region, sub_region,
                legal_classification, denomination_type,
                latitude, longitude, altitude_avg, topography, ocean_proximity,
                continental_influence, rivers,
                soils, climate_classification, thermal_amplitude, precipitation,
                sunshine, climate_risks, natural_influences,
                legislation_rules, max_yield, min_alcohol, aging_requirements,
                authorized_methods, restrictions,
                grapes_json, production_json, sensory_json, wine_styles_json,
                subregions_json, cities_json, micro_terroirs_json,
                history, particularities, technical_comparisons, official_references,
                geo_layer, leg_layer, ter_layer, uva_layer, tec_layer, sen_layer, hist_layer, com_layer,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                universal_id,
                d["name"], d["country"], d["macro_region"], d["sub_region"],
                d["legal_classification"], d["denomination_type"],
                d["latitude"], d["longitude"], d["altitude_avg"], d["topography"],
                d["ocean_proximity"], d["continental_influence"], d["rivers"],
                d["soils"], d["climate_classification"], d["thermal_amplitude"], d["precipitation"],
                d["sunshine"], d["climate_risks"], d["natural_influences"],
                d["legislation_rules"], d["max_yield"], d["min_alcohol"], d["aging_requirements"],
                d["authorized_methods"], d["restrictions"],
                d["grapes_json"], d["production_json"], d["sensory_json"], d["wine_styles_json"],
                d["subregions_json"], d["cities_json"], d["micro_terroirs_json"],
                d["history"], d["particularities"], d["technical_comparisons"], d["official_references"],
                "Hierarquia geográfica estruturada",
                "Regras legais da denominação",
                "Terroir detalhado",
                "Camada de castas e funções",
                "Camada de produção e vinificação",
                "Camada sensorial",
                "Camada histórica",
                "Camada comercial / estratégica",
                now, now
            ))

    conn.commit()
    conn.close()

# =====================================================================================
# CRUD / QUERY
# =====================================================================================

def get_all_denominations():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, universal_id, name, country, macro_region, sub_region,
               legal_classification, denomination_type, min_alcohol
        FROM denominations
        ORDER BY country, macro_region, sub_region, name
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_denomination_by_name(name: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM denominations WHERE name = ?", (name,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description] if cur.description else []
    conn.close()
    if row:
        return dict(zip(cols, row))
    return None

def get_denomination_by_id(row_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM denominations WHERE id = ?", (row_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description] if cur.description else []
    conn.close()
    if row:
        return dict(zip(cols, row))
    return None

def search_denominations(country=None, macro=None, legal=None, style=None, text=None):
    conn = get_conn()
    cur = conn.cursor()

    query = """
        SELECT id, universal_id, name, country, macro_region, sub_region,
               legal_classification, denomination_type
        FROM denominations
        WHERE 1=1
    """
    params = []

    if country and country != "Todos":
        query += " AND country = ?"
        params.append(country)

    if macro and macro != "Todos":
        query += " AND macro_region = ?"
        params.append(macro)

    if legal and legal != "Todos":
        query += " AND legal_classification = ?"
        params.append(legal)

    if text:
        query += " AND (name LIKE ? OR sub_region LIKE ? OR macro_region LIKE ? OR country LIKE ?)"
        like = f"%{text}%"
        params.extend([like, like, like, like])

    query += " ORDER BY country, macro_region, sub_region, name"
    cur.execute(query, params)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    conn.close()

    results = [dict(zip(cols, r)) for r in rows]

    if style and style != "Todos":
        filtered = []
        for r in results:
            full = get_denomination_by_id(r["id"])
            styles = from_json(full.get("wine_styles_json"))
            if style in styles:
                filtered.append(r)
        return filtered

    return results

def insert_or_update_denomination(payload: Dict[str, Any], record_id: Optional[int] = None):
    conn = get_conn()
    cur = conn.cursor()

    now = datetime.now().isoformat()
    universal_id = payload.get("universal_id") or generate_universal_id(
        payload.get("country", ""),
        payload.get("macro_region", ""),
        payload.get("sub_region", "")
    )

    fields = [
        "universal_id", "name", "country", "macro_region", "sub_region",
        "legal_classification", "denomination_type",
        "latitude", "longitude", "altitude_avg", "topography",
        "ocean_proximity", "continental_influence", "rivers",
        "soils", "climate_classification", "thermal_amplitude",
        "precipitation", "sunshine", "climate_risks", "natural_influences",
        "legislation_rules", "max_yield", "min_alcohol", "aging_requirements",
        "authorized_methods", "restrictions",
        "grapes_json", "production_json", "sensory_json", "wine_styles_json",
        "subregions_json", "cities_json", "micro_terroirs_json",
        "history", "particularities", "technical_comparisons", "official_references",
        "geo_layer", "leg_layer", "ter_layer", "uva_layer", "tec_layer", "sen_layer", "hist_layer", "com_layer"
    ]

    values = [
        universal_id,
        payload.get("name"),
        payload.get("country"),
        payload.get("macro_region"),
        payload.get("sub_region"),
        payload.get("legal_classification"),
        payload.get("denomination_type"),
        payload.get("latitude"),
        payload.get("longitude"),
        payload.get("altitude_avg"),
        payload.get("topography"),
        payload.get("ocean_proximity"),
        payload.get("continental_influence"),
        payload.get("rivers"),
        payload.get("soils"),
        payload.get("climate_classification"),
        payload.get("thermal_amplitude"),
        payload.get("precipitation"),
        payload.get("sunshine"),
        payload.get("climate_risks"),
        payload.get("natural_influences"),
        payload.get("legislation_rules"),
        payload.get("max_yield"),
        payload.get("min_alcohol"),
        payload.get("aging_requirements"),
        payload.get("authorized_methods"),
        payload.get("restrictions"),
        payload.get("grapes_json"),
        payload.get("production_json"),
        payload.get("sensory_json"),
        payload.get("wine_styles_json"),
        payload.get("subregions_json"),
        payload.get("cities_json"),
        payload.get("micro_terroirs_json"),
        payload.get("history"),
        payload.get("particularities"),
        payload.get("technical_comparisons"),
        payload.get("official_references"),
        payload.get("geo_layer"),
        payload.get("leg_layer"),
        payload.get("ter_layer"),
        payload.get("uva_layer"),
        payload.get("tec_layer"),
        payload.get("sen_layer"),
        payload.get("hist_layer"),
        payload.get("com_layer"),
    ]

    if record_id:
        set_clause = ", ".join([f"{f}=?" for f in fields]) + ", updated_at=?"
        sql = f"UPDATE denominations SET {set_clause} WHERE id=?"
        cur.execute(sql, values + [now, record_id])
    else:
        sql = f"""
        INSERT INTO denominations (
            {", ".join(fields)}, created_at, updated_at
        ) VALUES (
            {", ".join(["?"] * len(fields))}, ?, ?
        )
        """
        cur.execute(sql, values + [now, now])

    conn.commit()
    conn.close()

def save_audit(wine_name, denomination_name, vintage, alcohol, grape, country, result, errors):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO label_audits (
            wine_name, denomination_name, vintage, alcohol, grape, country,
            result, errors_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        wine_name, denomination_name, vintage, alcohol, grape, country,
        result, json.dumps(errors, ensure_ascii=False), datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_recent_audits(limit=50):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT wine_name, denomination_name, vintage, alcohol, grape, country, result, errors_json, created_at
        FROM label_audits
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

# =====================================================================================
# ENGINE DE AUDITORIA
# =====================================================================================

def audit_label(denomination: Dict[str, Any], wine_name: str, grape: str, alcohol: float, vintage: int):
    errors = []

    allowed_grapes = [g.get("grape") for g in from_json(denomination.get("grapes_json")) if isinstance(g, dict)]
    min_alcohol = denomination.get("min_alcohol")
    current_year = datetime.now().year

    if min_alcohol is not None and alcohol < float(min_alcohol):
        errors.append(
            f"Álcool abaixo do mínimo da denominação: rótulo {alcohol:.1f}% vol vs mínimo {float(min_alcohol):.1f}% vol."
        )

    if allowed_grapes and grape not in allowed_grapes:
        errors.append(
            f"A uva '{grape}' não consta entre as castas cadastradas para a denominação {denomination['name']}."
        )

    if vintage > current_year:
        errors.append(
            f"Safra futura/inválida: {vintage}."
        )

    if vintage < 1800:
        errors.append(
            f"Safra irrealisticamente antiga para validação automática: {vintage}."
        )

    result = "APROVADO" if not errors else "REPROVADO"
    return result, errors

# =====================================================================================
# RENDERIZAÇÃO DE FICHAS
# =====================================================================================

def render_denomination_card(d):
    st.markdown(f"## {d['name']}")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("ID Universal", d.get("universal_id", "—"))
        st.write(f"**País:** {d.get('country', '—')}")
        st.write(f"**Macro-região:** {d.get('macro_region', '—')}")
        st.write(f"**Sub-região:** {d.get('sub_region', '—')}")

    with c2:
        st.write(f"**Classificação legal:** {d.get('legal_classification', '—')}")
        st.write(f"**Tipo de denominação:** {d.get('denomination_type', '—')}")
        st.write(f"**Álcool mínimo:** {d.get('min_alcohol', '—')}")
        st.write(f"**Rendimento máximo:** {d.get('max_yield', '—')}")

    with c3:
        st.write(f"**Latitude:** {d.get('latitude', '—')}")
        st.write(f"**Longitude:** {d.get('longitude', '—')}")
        st.write(f"**Altitude média:** {d.get('altitude_avg', '—')}")
        st.write(f"**Topografia:** {d.get('topography', '—')}")

    with c4:
        st.write(f"**Proximidade oceânica:** {d.get('ocean_proximity', '—')}")
        st.write(f"**Influência continental:** {d.get('continental_influence', '—')}")
        st.write(f"**Rios relevantes:** {d.get('rivers', '—')}")

    st.markdown("---")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Terroir", "Legislação", "Castas", "Produção", "Sensorial", "Estrutura Expandida"
    ])

    with tab1:
        st.subheader("Solos")
        soils = from_json(d.get("soils"))
        if soils:
            for s in soils:
                badge(s, "#7c5638")
        st.write("")
        st.write(f"**Clima:** {d.get('climate_classification', '—')}")
        st.write(f"**Amplitude térmica:** {d.get('thermal_amplitude', '—')}")
        st.write(f"**Precipitação:** {d.get('precipitation', '—')}")
        st.write(f"**Insolação:** {d.get('sunshine', '—')}")
        st.write(f"**Riscos climáticos:** {d.get('climate_risks', '—')}")
        st.write(f"**Influências naturais:** {d.get('natural_influences', '—')}")

    with tab2:
        st.write(f"**Regras da DO:** {d.get('legislation_rules', '—')}")
        st.write(f"**Rendimento máximo:** {d.get('max_yield', '—')}")
        st.write(f"**Álcool mínimo:** {d.get('min_alcohol', '—')}")
        st.write(f"**Exigências de envelhecimento:** {d.get('aging_requirements', '—')}")
        st.write(f"**Métodos autorizados:** {d.get('authorized_methods', '—')}")
        st.write(f"**Restrições:** {d.get('restrictions', '—')}")

    with tab3:
        grapes = from_json(d.get("grapes_json"))
        if grapes:
            st.markdown("### Castas")
            for g in grapes:
                if isinstance(g, dict):
                    st.markdown(
                        f"""
                        **{g.get('grape', '—')}**  
                        - Função: {g.get('function', '—')}  
                        - Percentual / status: {g.get('percent_allowed', '—')}  
                        - Sensorial: {g.get('sensory', '—')}  
                        - Adaptação climática: {g.get('climatic_adaptation', '—')}
                        """
                    )
                    st.markdown("---")
        else:
            st.info("Sem castas cadastradas.")

    with tab4:
        prod = from_json(d.get("production_json"))
        if isinstance(prod, dict):
            st.write(f"**Colheita:** {prod.get('harvest', '—')}")
            st.write(f"**Prensagem:** {prod.get('pressing', '—')}")
            st.write(f"**Fermentação:** {prod.get('fermentation', '—')}")
            st.write(f"**Madeira:** {prod.get('wood_stage', '—')}")
            st.write(f"**Métodos tradicionais:** {prod.get('traditional_methods', '—')}")
            st.write(f"**Técnicas modernas:** {prod.get('modern_techniques', '—')}")
        else:
            st.info("Sem módulo de produção preenchido.")

    with tab5:
        sen = from_json(d.get("sensory_json"))
        if isinstance(sen, dict):
            st.write(f"**Aromas primários:** {', '.join(sen.get('primary_aromas', [])) if sen.get('primary_aromas') else '—'}")
            st.write(f"**Aromas secundários:** {', '.join(sen.get('secondary_aromas', [])) if sen.get('secondary_aromas') else '—'}")
            st.write(f"**Aromas terciários:** {', '.join(sen.get('tertiary_aromas', [])) if sen.get('tertiary_aromas') else '—'}")
            st.write(f"**Estrutura:** {sen.get('structure', '—')}")
            st.write(f"**Acidez:** {sen.get('acidity', '—')}")
            st.write(f"**Taninos:** {sen.get('tannins', '—')}")
            st.write(f"**Persistência:** {sen.get('finish', '—')}")
            st.write(f"**Potencial de guarda:** {sen.get('aging_potential', '—')}")
        else:
            st.info("Sem módulo sensorial preenchido.")

    with tab6:
        st.markdown("### Estilos produzidos")
        styles = from_json(d.get("wine_styles_json"))
        if styles:
            for s in styles:
                badge(s, "#2f6b4f")

        st.markdown("### Sub-regiões")
        subs = from_json(d.get("subregions_json"))
        if subs:
            st.write(", ".join(subs))
        else:
            st.write("—")

        st.markdown("### Cidades importantes")
        cities = from_json(d.get("cities_json"))
        if cities:
            st.write(", ".join(cities))
        else:
            st.write("—")

        st.markdown("### Micro-terroirs")
        micro = from_json(d.get("micro_terroirs_json"))
        if micro:
            for m in micro:
                st.write(f"- {m}")
        else:
            st.write("—")

        st.markdown("### História")
        st.write(d.get("history", "—"))

        st.markdown("### Particularidades")
        st.write(d.get("particularities", "—"))

        st.markdown("### Comparações técnicas")
        st.write(d.get("technical_comparisons", "—"))

        st.markdown("### Referências oficiais")
        st.write(d.get("official_references", "—"))

        st.markdown("### Camadas estruturais")
        st.write(f"**GEO:** {d.get('geo_layer', '—')}")
        st.write(f"**LEG:** {d.get('leg_layer', '—')}")
        st.write(f"**TER:** {d.get('ter_layer', '—')}")
        st.write(f"**UVA:** {d.get('uva_layer', '—')}")
        st.write(f"**TEC:** {d.get('tec_layer', '—')}")
        st.write(f"**SEN:** {d.get('sen_layer', '—')}")
        st.write(f"**HIST:** {d.get('hist_layer', '—')}")
        st.write(f"**COM:** {d.get('com_layer', '—')}")

# =====================================================================================
# SIDEBAR / NAVEGAÇÃO
# =====================================================================================

def sidebar_nav():
    st.sidebar.title("🍷 WINEINDEX OMEGA")
    st.sidebar.caption("V10 — Definitive Master Build")

    menu = st.sidebar.radio(
        "Módulos",
        [
            "Dashboard",
            "V1 — Auditor de Rótulos",
            "V2 — Explorer de Denominações",
            "V3 — Cadastro / Edição de DO",
            "Auditorias Salvas",
            "Arquitetura do Projeto"
        ]
    )
    return menu

# =====================================================================================
# DASHBOARD
# =====================================================================================

def render_dashboard():
    st.title("🍷 WINEINDEX OMEGA V10")
    st.caption("Definitive Master Build — auditoria de rótulos + atlas global de denominações + banco estruturado")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM denominations")
    total_dos = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT country) FROM denominations")
    total_countries = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM label_audits")
    total_audits = cur.fetchone()[0]

    conn.close()

    c1, c2, c3 = st.columns(3)
    c1.metric("Denominações cadastradas", total_dos)
    c2.metric("Países representados", total_countries)
    c3.metric("Auditorias salvas", total_audits)

    st.markdown("---")
    st.subheader("Versões integradas neste app")
    st.markdown("""
    **V1 — Auditor de Rótulos**
    - Valida álcool mínimo
    - Valida casta principal
    - Valida safra
    - Cruza rótulo com a denominação cadastrada

    **V2 — Explorer de Denominações**
    - Consulta DO/DOC/DOCG/AOC/DOCa etc.
    - Filtros por país / macro-região / tipo legal / estilo
    - Exibição completa por módulos: GEO, TER, LEG, UVA, TEC, SEN, HIST, COM

    **V3 — Omega Data Layer**
    - Banco SQLite
    - Cadastro e edição de denominações
    - Estrutura pronta para expansão massiva
    - IDs universais
    - Seed inicial (Sauternes, Barolo, Rioja)
    """)

# =====================================================================================
# V1 — AUDITOR DE RÓTULOS
# =====================================================================================

def render_v1_label_auditor():
    st.title("V1 — Auditor de Rótulos")
    st.write("Cruza os dados do rótulo com as regras cadastradas da denominação.")

    all_dos = get_all_denominations()
    do_names = [r[2] for r in all_dos]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Dados do rótulo")
        wine_name = st.text_input("Nome do vinho", "Meu Vinho")
        denomination_name = st.selectbox("Denominação declarada", do_names if do_names else [""])
        grape = st.text_input("Uva principal", "Merlot")
        alcohol = st.number_input("Teor alcoólico (% vol)", min_value=0.0, max_value=25.0, value=13.0, step=0.1)
        vintage = st.number_input("Safra", min_value=1800, max_value=2100, value=2022, step=1)

        run = st.button("Executar auditoria", use_container_width=True)

    with col2:
        st.subheader("Motor de conformidade")
        st.info("""
        Verificações atuais:
        - Álcool mínimo da denominação
        - Casta principal permitida
        - Safra futura / inválida
        - Registro da auditoria no banco
        """)

    if run:
        denom = get_denomination_by_name(denomination_name)
        if not denom:
            st.error("Denominação não encontrada.")
            return

        result, errors = audit_label(denom, wine_name, grape, alcohol, int(vintage))

        st.markdown("---")
        st.subheader("Resultado da Auditoria")

        if result == "APROVADO":
            st.success(f"✅ **{wine_name}** passou na auditoria para **{denomination_name}**.")
        else:
            st.error(f"❌ **{wine_name}** possui inconformidades para **{denomination_name}**.")
            for e in errors:
                st.write(f"- {e}")

        save_audit(
            wine_name=wine_name,
            denomination_name=denomination_name,
            vintage=int(vintage),
            alcohol=float(alcohol),
            grape=grape,
            country=denom.get("country"),
            result=result,
            errors=errors
        )

        st.markdown("### Base comparada")
        st.write(f"**DO selecionada:** {denom.get('name')}")
        st.write(f"**País:** {denom.get('country')}")
        st.write(f"**Classificação legal:** {denom.get('legal_classification')}")
        st.write(f"**Álcool mínimo cadastrado:** {denom.get('min_alcohol')}")

        grapes = [g.get("grape") for g in from_json(denom.get("grapes_json")) if isinstance(g, dict)]
        st.write(f"**Castas cadastradas:** {', '.join(grapes) if grapes else '—'}")

# =====================================================================================
# V2 — EXPLORER DE DENOMINAÇÕES
# =====================================================================================

def render_v2_explorer():
    st.title("V2 — Explorer de Denominações")
    st.write("Consulta estruturada do índice global de denominações.")

    all_rows = get_all_denominations()
    countries = sorted(list({r[3] for r in all_rows if r[3]}))
    macros = sorted(list({r[4] for r in all_rows if r[4]}))
    legals = sorted(list({r[6] for r in all_rows if r[6]}))

    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 2])

    with c1:
        country = st.selectbox("País", ["Todos"] + countries)
    with c2:
        macro = st.selectbox("Macro-região", ["Todos"] + macros)
    with c3:
        legal = st.selectbox("Classificação legal", ["Todos"] + legals)
    with c4:
        style = st.selectbox("Estilo", ["Todos"] + WINE_STYLES)
    with c5:
        text = st.text_input("Busca livre", "")

    results = search_denominations(country, macro, legal, style, text)

    st.markdown(f"### Resultados encontrados: {len(results)}")

    if not results:
        st.warning("Nenhuma denominação encontrada com esses filtros.")
        return

    labels = [f"{r['name']} | {r['country']} | {r['macro_region']} | {r['sub_region']}" for r in results]
    selected_label = st.selectbox("Selecione uma denominação", labels)

    selected_name = selected_label.split(" | ")[0]
    d = get_denomination_by_name(selected_name)

    if d:
        st.markdown("---")
        render_denomination_card(d)

# =====================================================================================
# V3 — CADASTRO / EDIÇÃO DE DO
# =====================================================================================

def render_v3_editor():
    st.title("V3 — Cadastro / Edição de Denominações")
    st.write("Camada Omega de alimentação e manutenção do banco.")

    all_rows = get_all_denominations()
    edit_options = ["[NOVA DENOMINAÇÃO]"] + [
        f"{r[0]} — {r[2]} ({r[3]} / {r[4]} / {r[5]})" for r in all_rows
    ]
    selected = st.selectbox("Selecionar registro para editar", edit_options)

    record = None
    record_id = None
    if selected != "[NOVA DENOMINAÇÃO]":
        record_id = int(selected.split(" — ")[0])
        record = get_denomination_by_id(record_id)

    def v(field, default=""):
        if record:
            return record.get(field, default)
        return default

    st.markdown("## Identificação")
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("Nome da região / denominação", v("name", ""))
        country = st.text_input("País", v("country", ""))
        macro_region = st.text_input("Região macro", v("macro_region", ""))
    with c2:
        sub_region = st.text_input("Sub-região", v("sub_region", ""))
        legal_classification = st.selectbox(
            "Classificação legal",
            LEGAL_TYPES,
            index=LEGAL_TYPES.index(v("legal_classification")) if v("legal_classification") in LEGAL_TYPES else 0
        )
        denomination_type = st.text_input("Tipo de denominação", v("denomination_type", "Denominação de Origem"))
    with c3:
        latitude = st.number_input("Latitude", value=safe_float(v("latitude", 0.0)), format="%.6f")
        longitude = st.number_input("Longitude", value=safe_float(v("longitude", 0.0)), format="%.6f")
        altitude_avg = st.number_input("Altitude média", value=safe_float(v("altitude_avg", 0.0)), format="%.2f")

    st.markdown("## Geografia e terroir")
    c1, c2 = st.columns(2)
    with c1:
        topography = st.text_area("Topografia", v("topography", ""), height=80)
        ocean_proximity = st.text_input("Proximidade oceânica", v("ocean_proximity", ""))
        continental_influence = st.text_input("Influência continental", v("continental_influence", ""))
        rivers = st.text_input("Rios relevantes", v("rivers", ""))
        soils = st.multiselect(
            "Solos",
            SOIL_TAXONOMY,
            default=from_json(v("soils", "[]"))
        )
    with c2:
        climate_classification = st.selectbox(
            "Clima",
            CLIMATE_TAXONOMY,
            index=CLIMATE_TAXONOMY.index(v("climate_classification")) if v("climate_classification") in CLIMATE_TAXONOMY else 0
        )
        thermal_amplitude = st.text_input("Amplitude térmica", v("thermal_amplitude", ""))
        precipitation = st.text_input("Precipitação", v("precipitation", ""))
        sunshine = st.text_input("Insolação", v("sunshine", ""))
        climate_risks = st.text_area("Riscos climáticos", v("climate_risks", ""), height=80)
        natural_influences = st.text_area("Influências naturais", v("natural_influences", ""), height=80)

    st.markdown("## Legislação")
    c1, c2 = st.columns(2)
    with c1:
        legislation_rules = st.text_area("Regras da DO", v("legislation_rules", ""), height=120)
        max_yield = st.text_input("Rendimento máximo", v("max_yield", ""))
        min_alcohol = st.number_input("Álcool mínimo", value=safe_float(v("min_alcohol", 12.0)), format="%.1f")
    with c2:
        aging_requirements = st.text_area("Exigências de envelhecimento", v("aging_requirements", ""), height=120)
        authorized_methods = st.text_area("Métodos autorizados", v("authorized_methods", ""), height=120)
        restrictions = st.text_area("Restrições", v("restrictions", ""), height=120)

    st.markdown("## Castas")
    grapes_raw = st.text_area(
        "Castas em JSON",
        value=v("grapes_json", json.dumps([
            {
                "grape": "Exemplo",
                "function": "Base",
                "percent_allowed": "Principal",
                "sensory": "Fruta / estrutura",
                "climatic_adaptation": "Boa"
            }
        ], ensure_ascii=False, indent=2)),
        height=220
    )

    st.markdown("## Produção e vinificação")
    production_raw = st.text_area(
        "Produção em JSON",
        value=v("production_json", json.dumps({
            "harvest": "",
            "pressing": "",
            "fermentation": "",
            "wood_stage": "",
            "traditional_methods": "",
            "modern_techniques": ""
        }, ensure_ascii=False, indent=2)),
        height=220
    )

    st.markdown("## Sensorial")
    sensory_raw = st.text_area(
        "Sensorial em JSON",
        value=v("sensory_json", json.dumps({
            "primary_aromas": [],
            "secondary_aromas": [],
            "tertiary_aromas": [],
            "structure": "",
            "acidity": "",
            "tannins": "",
            "finish": "",
            "aging_potential": ""
        }, ensure_ascii=False, indent=2)),
        height=240
    )

    st.markdown("## Estilos, sub-regiões, cidades e micro-terroirs")
    c1, c2 = st.columns(2)
    with c1:
        wine_styles = st.multiselect(
            "Estilos produzidos",
            WINE_STYLES,
            default=from_json(v("wine_styles_json", "[]"))
        )
        subregions_text = st.text_area(
            "Sub-regiões (uma por linha)",
            "\n".join(from_json(v("subregions_json", "[]"))),
            height=120
        )
    with c2:
        cities_text = st.text_area(
            "Cidades importantes (uma por linha)",
            "\n".join(from_json(v("cities_json", "[]"))),
            height=120
        )
        micro_text = st.text_area(
            "Micro-terroirs (um por linha)",
            "\n".join(from_json(v("micro_terroirs_json", "[]"))),
            height=120
        )

    st.markdown("## História, particularidades e referências")
    history = st.text_area("História", v("history", ""), height=120)
    particularities = st.text_area("Particularidades", v("particularities", ""), height=120)
    technical_comparisons = st.text_area("Comparações técnicas", v("technical_comparisons", ""), height=120)
    official_references = st.text_area("Referências oficiais", v("official_references", ""), height=120)

    st.markdown("## Camadas estruturais")
    c1, c2 = st.columns(2)
    with c1:
        geo_layer = st.text_area("GEO", v("geo_layer", "Hierarquia geográfica"), height=80)
        leg_layer = st.text_area("LEG", v("leg_layer", "Legislação"), height=80)
        ter_layer = st.text_area("TER", v("ter_layer", "Terroir"), height=80)
        uva_layer = st.text_area("UVA", v("uva_layer", "Castas"), height=80)
    with c2:
        tec_layer = st.text_area("TEC", v("tec_layer", "Métodos produtivos"), height=80)
        sen_layer = st.text_area("SEN", v("sen_layer", "Sensorial"), height=80)
        hist_layer = st.text_area("HIST", v("hist_layer", "História"), height=80)
        com_layer = st.text_area("COM", v("com_layer", "Comercial / mercado"), height=80)

    if st.button("Salvar denominação", use_container_width=True):
        try:
            json.loads(grapes_raw)
            json.loads(production_raw)
            json.loads(sensory_raw)
        except Exception as e:
            st.error(f"Erro em um dos campos JSON: {e}")
            return

        payload = {
            "name": name,
            "country": country,
            "macro_region": macro_region,
            "sub_region": sub_region,
            "legal_classification": legal_classification,
            "denomination_type": denomination_type,
            "latitude": latitude,
            "longitude": longitude,
            "altitude_avg": altitude_avg,
            "topography": topography,
            "ocean_proximity": ocean_proximity,
            "continental_influence": continental_influence,
            "rivers": rivers,
            "soils": to_json(soils),
            "climate_classification": climate_classification,
            "thermal_amplitude": thermal_amplitude,
            "precipitation": precipitation,
            "sunshine": sunshine,
            "climate_risks": climate_risks,
            "natural_influences": natural_influences,
            "legislation_rules": legislation_rules,
            "max_yield": max_yield,
            "min_alcohol": min_alcohol,
            "aging_requirements": aging_requirements,
            "authorized_methods": authorized_methods,
            "restrictions": restrictions,
            "grapes_json": grapes_raw,
            "production_json": production_raw,
            "sensory_json": sensory_raw,
            "wine_styles_json": to_json(wine_styles),
            "subregions_json": to_json([x.strip() for x in subregions_text.splitlines() if x.strip()]),
            "cities_json": to_json([x.strip() for x in cities_text.splitlines() if x.strip()]),
            "micro_terroirs_json": to_json([x.strip() for x in micro_text.splitlines() if x.strip()]),
            "history": history,
            "particularities": particularities,
            "technical_comparisons": technical_comparisons,
            "official_references": official_references,
            "geo_layer": geo_layer,
            "leg_layer": leg_layer,
            "ter_layer": ter_layer,
            "uva_layer": uva_layer,
            "tec_layer": tec_layer,
            "sen_layer": sen_layer,
            "hist_layer": hist_layer,
            "com_layer": com_layer,
        }

        insert_or_update_denomination(payload, record_id=record_id)
        st.success("Denominação salva com sucesso.")

# =====================================================================================
# AUDITORIAS SALVAS
# =====================================================================================

def render_saved_audits():
    st.title("Auditorias salvas")
    rows = get_recent_audits(100)

    if not rows:
        st.info("Nenhuma auditoria registrada ainda.")
        return

    for row in rows:
        wine_name, denomination_name, vintage, alcohol, grape, country, result, errors_json, created_at = row
        errors = from_json(errors_json)

        with st.expander(f"{created_at[:19]} | {wine_name} | {denomination_name} | {result}"):
            st.write(f"**Vinho:** {wine_name}")
            st.write(f"**Denominação:** {denomination_name}")
            st.write(f"**País:** {country}")
            st.write(f"**Safra:** {vintage}")
            st.write(f"**Álcool:** {alcohol}")
            st.write(f"**Uva:** {grape}")
            st.write(f"**Resultado:** {result}")

            if errors:
                st.write("**Inconformidades:**")
                for e in errors:
                    st.write(f"- {e}")
            else:
                st.success("Sem inconformidades detectadas nas regras atuais.")

# =====================================================================================
# ARQUITETURA DO PROJETO
# =====================================================================================

def render_architecture():
    st.title("Arquitetura do Projeto")
    st.markdown("""
# WINEINDEX OMEGA V10 — DEFINITIVE MASTER BUILD

## Estrutura consolidada
### V1 — Label Audit Engine
Motor de auditoria de rótulos baseado em:
- denominação declarada
- castas permitidas
- álcool mínimo
- safra
- regras legais mínimas visíveis

### V2 — Global Index Explorer
Camada enciclopédica / atlas técnico:
- identificação
- geografia
- terroir
- legislação
- castas
- vinificação
- perfil sensorial
- estilos
- sub-regiões
- cidades
- micro-terroirs
- história
- comparações técnicas
- referências oficiais

### V3 — Omega Data Engine
Camada de persistência e expansão:
- SQLite
- CRUD de denominações
- IDs universais
- armazenamento de auditorias
- seed inicial
- pronto para evoluir para ingestão massiva

## Próximo salto lógico (V11)
Se você quiser transformar isso no núcleo do **INDEX MUNDIAL DEFINITIVO**, o próximo passo é quebrar em módulos:

- `app.py` → interface
- `db.py` → banco e queries
- `seed.py` → seeds por país
- `audit_engine.py` → motor de conformidade
- `models.py` → schemas e taxonomias
- `importers/` → importadores por país
- `country_modules/france.py`
- `country_modules/italy.py`
- `country_modules/spain.py`
- `country_modules/portugal.py`

E depois adicionar:
- importação em lote por CSV / JSON
- score de completude da DO
- painel de progresso do INDEX
- mapa global
- árvore hierárquica País > Região > DO > Subzona > Micro-terroir
- exportação para Excel / CSV / PDF
""")

# =====================================================================================
# MAIN
# =====================================================================================

def main():
    init_db()
    seed_if_empty()

    menu = sidebar_nav()

    if menu == "Dashboard":
        render_dashboard()
    elif menu == "V1 — Auditor de Rótulos":
        render_v1_label_auditor()
    elif menu == "V2 — Explorer de Denominações":
        render_v2_explorer()
    elif menu == "V3 — Cadastro / Edição de DO":
        render_v3_editor()
    elif menu == "Auditorias Salvas":
        render_saved_audits()
    elif menu == "Arquitetura do Projeto":
        render_architecture()

if __name__ == "__main__":
    main()
