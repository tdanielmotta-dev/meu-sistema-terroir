import sqlite3
from datetime import datetime
import streamlit as st

# =========================================================
# WINEINDEX OMEGA — STABLE CLOUD BUILD
# =========================================================

DB_NAME = "wineindex.db"


# =========================================================
# DATABASE
# =========================================================
def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS denominations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        universal_id TEXT UNIQUE NOT NULL,
        country TEXT NOT NULL,
        macro_region TEXT,
        sub_region TEXT NOT NULL,
        appellation_name TEXT NOT NULL,
        legal_level TEXT,
        wine_color_scope TEXT,
        alcohol_min REAL,
        alcohol_max REAL,
        vintage_max INTEGER,
        allowed_grapes TEXT,
        notes TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def seed_if_empty():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM denominations")
    total = cur.fetchone()[0]

    if total == 0:
        now = datetime.utcnow().isoformat()

        seed_rows = [
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
                "Seed inicial Bordeaux Graves.",
                now,
                now
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
                "Seed inicial Bordeaux Sauternes.",
                now,
                now
            ),
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
                "Seed inicial Piemonte Barolo.",
                now,
                now
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
                "Seed inicial Piemonte Barbaresco.",
                now,
                now
            ),
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
                "Seed inicial Rioja.",
                now,
                now
            ),
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
                "Seed inicial Brasil Mantiqueira.",
                now,
                now
            )
        ]

        cur.executemany("""
        INSERT OR IGNORE INTO denominations (
            universal_id,
            country,
            macro_region,
            sub_region,
            appellation_name,
            legal_level,
            wine_color_scope,
            alcohol_min,
            alcohol_max,
            vintage_max,
            allowed_grapes,
            notes,
            created_at,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_rows)

    conn.commit()
    conn.close()


# =========================================================
# DATA ACCESS
# =========================================================
def get_all_denominations():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            universal_id,
            country,
            macro_region,
            sub_region,
            appellation_name,
            legal_level,
            wine_color_scope,
            alcohol_min,
            alcohol_max,
            vintage_max,
            allowed_grapes,
            notes
        FROM denominations
        ORDER BY country, macro_region, sub_region
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_appellation_by_name(appellation_name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            universal_id,
            country,
            macro_region,
            sub_region,
            appellation_name,
            legal_level,
            wine_color_scope,
            alcohol_min,
            alcohol_max,
            vintage_max,
            allowed_grapes,
            notes
        FROM denominations
        WHERE appellation_name = ?
        LIMIT 1
    """, (appellation_name,))
    row = cur.fetchone()
    conn.close()
    return row


# =========================================================
# AUDIT ENGINE
# =========================================================
def audit_label(nome, uva, alcool, safra, appellation_name):
    row = get_appellation_by_name(appellation_name)
    if not row:
        return [f"Denominação '{appellation_name}' não encontrada no banco."]

    (
        universal_id,
        country,
        macro_region,
        sub_region,
        appellation_name,
        legal_level,
        wine_color_scope,
        alcohol_min,
        alcohol_max,
        vintage_max,
        allowed_grapes,
        notes
    ) = row

    erros = []

    # álcool mínimo
    if alcohol_min is not None and alcool < alcohol_min:
        erros.append(
            f"Álcool abaixo do mínimo exigido pela denominação ({alcool}% < {alcohol_min}%)."
        )

    # álcool máximo
    if alcohol_max is not None and alcool > alcohol_max:
        erros.append(
            f"Álcool acima do máximo permitido ({alcool}% > {alcohol_max}%)."
        )

    # safra
    if vintage_max is not None and safra > vintage_max:
        erros.append(
            f"Ano de safra inválido/futuro para a regra atual da base ({safra} > {vintage_max})."
        )

    # uvas permitidas
    if allowed_grapes:
        permitted = [x.strip().lower() for x in allowed_grapes.split(";")]
        if uva.strip().lower() not in permitted:
            erros.append(
                f"A uva '{uva}' não consta entre as castas permitidas para {appellation_name}."
            )

    return erros


# =========================================================
# UI
# =========================================================
def main():
    st.set_page_config(page_title="WINEINDEX OMEGA", page_icon="🍷", layout="wide")

    init_db()
    seed_if_empty()

    st.title("🍷 WINEINDEX OMEGA")
    st.caption("Fiscalizador de rótulos + base inicial de denominações de origem")

    tabs = st.tabs([
        "Auditoria de Rótulo",
        "Base de Denominações",
        "Diagnóstico do Banco"
    ])

    # -----------------------------------------------------
    # TAB 1 - AUDITORIA
    # -----------------------------------------------------
    with tabs[0]:
        st.subheader("🔎 Auditoria de rótulo")

        all_rows = get_all_denominations()
        appellations = [r[4] for r in all_rows]

        col1, col2 = st.columns([1, 1])

        with col1:
            nome = st.text_input("Nome do vinho", "Meu Vinho Reserva")
            appellation = st.selectbox("Denominação / Região declarada", appellations)
            uva = st.selectbox(
                "Uva principal",
                [
                    "Merlot", "Cabernet Sauvignon", "Cabernet Franc",
                    "Sémillon", "Sauvignon Blanc", "Muscadelle",
                    "Nebbiolo", "Tempranillo", "Garnacha",
                    "Graciano", "Viura", "Chardonnay", "Pinot Noir", "Syrah"
                ]
            )

        with col2:
            alcool = st.number_input(
                "Teor alcoólico (% vol)",
                min_value=5.0,
                max_value=20.0,
                value=13.0,
                step=0.1
            )
            safra = st.number_input(
                "Ano da safra",
                min_value=1900,
                max_value=2035,
                value=2024
            )

        if st.button("Executar auditoria"):
            erros = audit_label(nome, uva, alcool, safra, appellation)

            if erros:
                st.error(f"❌ {nome} apresenta inconformidades:")
                for e in erros:
                    st.write(f"- {e}")
            else:
                st.success(f"✅ {nome} está conforme as regras visíveis parametrizadas para {appellation}.")

    # -----------------------------------------------------
    # TAB 2 - BASE
    # -----------------------------------------------------
    with tabs[1]:
        st.subheader("📚 Base inicial de denominações")

        rows = get_all_denominations()

        for r in rows:
            (
                universal_id,
                country,
                macro_region,
                sub_region,
                appellation_name,
                legal_level,
                wine_color_scope,
                alcohol_min,
                alcohol_max,
                vintage_max,
                allowed_grapes,
                notes
            ) = r

            with st.expander(f"{appellation_name} — {country} / {macro_region} / {sub_region}"):
                st.markdown(f"**ID:** {universal_id}")
                st.markdown(f"**Nível legal:** {legal_level}")
                st.markdown(f"**Escopo de estilos:** {wine_color_scope}")
                st.markdown(f"**Álcool mínimo:** {alcohol_min if alcohol_min is not None else '-'}")
                st.markdown(f"**Álcool máximo:** {alcohol_max if alcohol_max is not None else '-'}")
                st.markdown(f"**Safra máxima cadastrada:** {vintage_max if vintage_max is not None else '-'}")
                st.markdown(f"**Castas permitidas:** {allowed_grapes}")
                st.markdown(f"**Notas:** {notes}")

    # -----------------------------------------------------
    # TAB 3 - DIAGNÓSTICO
    # -----------------------------------------------------
    with tabs[2]:
        st.subheader("🛠 Diagnóstico do banco")

        rows = get_all_denominations()
        st.write(f"Total de denominações carregadas: **{len(rows)}**")

        st.code("""
Se esta aba abriu e mostrou registros, o seed funcionou.
Se der erro novamente, o problema não está mais no INSERT principal,
e sim em algum trecho antigo do app.py ainda publicado no repositório.
        """)


if __name__ == "__main__":
    main()
