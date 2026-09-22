import streamlit as st
import datetime as dt
from providers import YahooFinanceProvider
from llm_providers import GroqClient
from agent_core import FinancialAgent

NOME_APP = "Bússola Capital"
TAGLINE = "Inteligência para investir"

st.set_page_config(
    page_title=NOME_APP,
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# ESTILO VISUAL
# ============================================================
st.markdown(
    """
    <style>
    :root{
        --bg:#0b1220;
        --bg-2:#0f1724;
        --panel:#121c2b;
        --panel-2:#152131;
        --border:#2b394b;
        --border-soft:rgba(148,163,184,.16);
        --text:#f3f6fb;
        --muted:#97a6bd;
        --muted-2:#73839b;
        --accent:#4fd1a5;
        --accent-2:#5ee7b5;
        --accent-soft:rgba(79,209,165,.12);
        --warning:#f6ad2f;
        --danger:#ff7b72;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background:
            radial-gradient(circle at 58% 10%, rgba(36,56,84,.12), transparent 28%),
            linear-gradient(180deg, #0b1220 0%, #09111c 100%) !important;
        color: var(--text);
    }

    [data-testid="stAppViewContainer"] > .main {
        background: transparent;
    }

    .block-container {
        max-width: 1460px;
        padding-top: 1.75rem;
        padding-bottom: 1rem;
        padding-left: 2.55rem;
        padding-right: 2.55rem;
    }

    /* ---------------- Sidebar ---------------- */
    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(16,28,42,.98), rgba(13,24,38,.98)) !important;
        border-right: 1px solid rgba(148,163,184,.06);
        min-width: 270px !important;
        width: 270px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.15rem;
    }

    .brand-wrap{
        display:flex;
        align-items:center;
        gap:.85rem;
        margin:.2rem .2rem 2rem .2rem;
    }

    .brand-logo{
        width:50px;
        height:50px;
        border-radius:50%;
        border:3px solid var(--accent);
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:24px;
        box-shadow:0 0 0 1px rgba(79,209,165,.12), inset 0 0 20px rgba(79,209,165,.06);
        color:var(--accent);
        flex:0 0 auto;
    }

    .brand-title{
        font-size:1.2rem;
        line-height:1.1;
        font-weight:800;
        margin:0;
        color:#fff;
        letter-spacing:-.02em;
    }

    .brand-sub{
        font-size:.79rem;
        margin:.32rem 0 0;
        color:#91a1b7;
    }

    [data-testid="stSidebar"] [role="radiogroup"] {
        gap:.62rem;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        background:transparent;
        border-radius:9px;
        padding:.88rem .82rem;
        margin:0;
        transition:.18s ease;
        border-left:3px solid transparent;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover{
        background:rgba(255,255,255,.035);
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){
        background:linear-gradient(90deg, rgba(79,209,165,.12), rgba(79,209,165,.07));
        border-left-color:var(--accent);
    }

    [data-testid="stSidebar"] [role="radiogroup"] label p{
        color:#c7d2e2 !important;
        font-size:.94rem;
        font-weight:500;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p{
        color:#fff !important;
        font-weight:700;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] hr {
        border-color:rgba(148,163,184,.18);
    }

    .sidebar-note{
        display:flex;
        gap:.8rem;
        align-items:flex-start;
        color:#8ea0b7;
        font-size:.78rem;
        line-height:1.45;
        border-top:1px solid rgba(148,163,184,.18);
        padding-top:1.25rem;
        margin-top:18rem;
    }

    .sidebar-note-icon{
        font-size:1.2rem;
        color:#a9b8ca;
    }

    /* ---------------- Tipografia ---------------- */
    h1,h2,h3,p,span,div{
        font-family: "Inter", "Segoe UI", Arial, sans-serif;
    }

    .page-title{
        font-size:2.55rem;
        line-height:1.05;
        font-weight:800;
        margin:0;
        color:#f8fafc;
        letter-spacing:-.035em;
    }

    .page-subtitle{
        font-size:1.03rem;
        color:#9aa9bf;
        margin:.55rem 0 1.65rem;
    }

    .asset-title{
        font-size:2.15rem;
        font-weight:800;
        line-height:1;
        margin:0;
        color:#f7f9fc;
        letter-spacing:-.03em;
    }

    .asset-name{
        color:#93a3ba;
        font-size:1rem;
        margin:.45rem 0 0;
    }

    /* ---------------- Pílulas / badges ---------------- */
    .pill{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        border-radius:10px;
        padding:.34rem .78rem;
        font-size:.77rem;
        line-height:1;
        font-weight:700;
        vertical-align:middle;
        margin-left:.45rem;
    }

    .pill-green{
        background:rgba(79,209,165,.10);
        color:#8cebc9;
        border:1px solid rgba(79,209,165,.22);
        padding:.7rem 1rem;
        border-radius:8px;
        margin-left:0;
    }

    .pill-gray{
        background:#202c3d;
        border:1px solid #27364a;
        color:#e4eaf2;
        margin-left:.65rem;
    }

    /* ---------------- Inputs e botão ---------------- */
    [data-testid="stTextInput"] input{
        min-height:50px;
        border-radius:8px !important;
        background:#101927 !important;
        border:1px solid #4a5a70 !important;
        color:#f7f9fc !important;
        font-size:.98rem !important;
        padding-left:1rem !important;
        box-shadow:none !important;
    }

    [data-testid="stTextInput"] input:focus{
        border-color:#688099 !important;
        box-shadow:0 0 0 1px rgba(104,128,153,.12) !important;
    }

    [data-testid="stTextInput"] input::placeholder{
        color:#73839a !important;
    }

    [data-testid="stButton"] > button{
        min-height:50px;
        width:100%;
        border-radius:8px !important;
        border:0 !important;
        font-weight:800 !important;
        font-size:.93rem !important;
        transition:.18s ease;
    }

    [data-testid="stButton"] > button[kind="primary"]{
        background:linear-gradient(135deg, #4cd6a7, #55d9a9) !important;
        color:#07130e !important;
        box-shadow:0 8px 18px rgba(79,209,165,.08);
    }

    [data-testid="stButton"] > button[kind="primary"]:hover{
        filter:brightness(1.04);
        transform:translateY(-1px);
    }

    .search-caption{
        color:#71839d;
        font-size:.75rem;
        margin-top:-.15rem;
    }

    /* ---------------- Cards ---------------- */
    .card{
        background:
            linear-gradient(180deg, rgba(20,31,47,.96), rgba(17,27,42,.96));
        border:1px solid rgba(91,109,134,.42);
        border-radius:9px;
        box-shadow:inset 0 1px 0 rgba(255,255,255,.015);
    }

    .metric-bar{
        padding:1.15rem 1.2rem;
        margin-top:1.2rem;
        margin-bottom:1.35rem;
    }

    .metric-row{
        display:grid;
        grid-template-columns:1fr 1fr 1fr;
        align-items:center;
    }

    .metric-item{
        display:grid;
        grid-template-columns:52px 1fr;
        align-items:center;
        gap:.72rem;
        padding:.1rem 1.35rem;
        min-height:62px;
    }

    .metric-item + .metric-item{
        border-left:1px solid rgba(148,163,184,.22);
    }

    .metric-icon{
        width:44px;
        height:44px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#b6c5da;
        font-size:1.55rem;
    }

    .metric-label{
        margin:0 0 .18rem;
        color:#a0adc0;
        font-size:.76rem;
    }

    .metric-value{
        margin:0;
        color:#f4f7fb;
        font-size:1.45rem;
        line-height:1.1;
        font-weight:800;
        letter-spacing:-.025em;
    }

    .panel{
        min-height:340px;
        padding:1.4rem 1.6rem 1.1rem;
    }

    .panel-title-row{
        display:flex;
        align-items:center;
        gap:.72rem;
        margin-bottom:.15rem;
    }

    .panel-icon{
        color:#b8c5d8;
        font-size:1.25rem;
    }

    .card-title{
        font-size:1.14rem;
        font-weight:800;
        margin:0;
        color:#f3f6fb;
    }

    .card-sub{
        font-size:.8rem;
        color:#91a0b6;
        margin:.38rem 0 1.2rem;
    }

    .info-table{
        border-top:1px solid rgba(148,163,184,.18);
        margin-top:1.05rem;
    }

    .info-row{
        display:grid;
        grid-template-columns:36% 64%;
        padding:.92rem 0;
        border-bottom:1px solid rgba(148,163,184,.18);
        align-items:center;
        font-size:.9rem;
    }

    .info-label{
        color:#9aa9bf;
    }

    .info-value{
        color:#f0f4f9;
        font-weight:600;
    }

    .ai-panel{
        display:flex;
        flex-direction:column;
    }

    .ai-content{
        min-height:214px;
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center;
        flex-direction:column;
        padding:.5rem .9rem 1rem;
    }

    .ai-summary{
        color:#d8e0eb;
        line-height:1.65;
        font-size:.92rem;
        text-align:left;
        width:100%;
        margin-top:.3rem;
    }

    .warning-icon{
        color:var(--warning);
        font-size:2.65rem;
        line-height:1;
        margin-bottom:.6rem;
    }

    .unavailable-title{
        font-weight:800;
        color:#f1f5f9;
        font-size:1rem;
        margin:.25rem 0;
    }

    .unavailable-text{
        color:#91a0b6;
        font-size:.82rem;
        line-height:1.45;
        margin:0;
    }

    .retry-like{
        border:1px solid #718096;
        border-radius:7px;
        padding:.78rem 1rem;
        margin-top:.9rem;
        width:100%;
        color:#eef2f7;
        font-weight:700;
        background:rgba(255,255,255,.01);
    }

    .verdict{
        margin-top:1rem;
        background:linear-gradient(135deg, rgba(79,209,165,.12), rgba(16,27,42,.96));
        border:1px solid rgba(79,209,165,.45);
        color:#e9fff7;
        border-radius:9px;
        padding:.95rem 1rem;
        font-size:.95rem;
        font-weight:700;
        text-align:center;
    }

    .card-forte,
    .card-risco{
        border-radius:9px;
        padding:.82rem .95rem;
        margin-bottom:.62rem;
        font-size:.9rem;
        line-height:1.45;
    }

    .card-forte{
        background:rgba(79,209,165,.08);
        border:1px solid rgba(79,209,165,.28);
    }

    .card-risco{
        background:rgba(255,123,114,.08);
        border:1px solid rgba(255,123,114,.28);
    }

    /* ---------------- Auxiliares ---------------- */
    .top-note{
        display:flex;
        align-items:center;
        justify-content:flex-end;
        color:#90a0b6;
        font-size:.78rem;
        padding-top:.9rem;
    }

    .top-note span{
        margin-left:.45rem;
    }

    .footer-line{
        border-top:1px solid rgba(148,163,184,.22);
        margin-top:1.4rem;
        padding-top:.85rem;
    }

    .footer{
        display:flex;
        justify-content:space-between;
        color:#72839a;
        font-size:.72rem;
    }

    div[data-testid="stExpander"]{
        background:transparent !important;
        border:0 !important;
    }

    div[data-testid="stExpander"] details{
        border-top:1px solid rgba(148,163,184,.18);
        border-radius:0;
    }

    div[data-testid="stExpander"] summary p{
        color:#c4cfdd !important;
        font-size:.8rem !important;
    }

    [data-testid="stCaptionContainer"]{
        color:#788aa3 !important;
    }

    #MainMenu,
    header[data-testid="stHeader"],
    footer{
        visibility:hidden;
    }

    /* ---------------- Responsivo ---------------- */
    @media (max-width: 1100px){
        .block-container{
            padding-left:1.4rem;
            padding-right:1.4rem;
        }

        .page-title{
            font-size:2.1rem;
        }

        .metric-row{
            grid-template-columns:1fr;
        }

        .metric-item + .metric-item{
            border-left:0;
            border-top:1px solid rgba(148,163,184,.18);
            padding-top:1rem;
            margin-top:.65rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FUNÇÕES DE APOIO
# ============================================================
@st.cache_data(ttl=600, show_spinner=False)
def buscar_dados(ticker: str):
    provider = YahooFinanceProvider()
    return provider.get_asset_quote(ticker)


@st.cache_resource(show_spinner=False)
def criar_agente():
    return FinancialAgent(
        data_provider=YahooFinanceProvider(),
        llm_client=GroqClient(),
    )


@st.cache_data(ttl=600, show_spinner=False)
def analisar_com_ia(ticker: str):
    """Análise cacheada por 10 min: evita chamar a Groq a cada rerun."""
    agent = FinancialAgent(
        data_provider=YahooFinanceProvider(),
        llm_client=GroqClient(),
    )
    quote = YahooFinanceProvider().get_asset_quote(ticker)
    return agent.run_analysis(ticker, quote=quote)


def para_pt(s: str) -> str:
    """Converte 1,234.56 para 1.234,56 (padrão brasileiro)."""
    return s.replace(",", "@").replace(".", ",").replace("@", ".")


def formatar_moeda(valor: float, moeda: str) -> str:
    simbolo = {"BRL": "R$", "USD": "US$"}.get(moeda, moeda)
    return f"{simbolo} {para_pt(f'{valor:,.2f}')}"


def formatar_valor_grande(valor):
    if valor is None:
        return "—"
    if valor >= 1_000_000_000:
        return para_pt(f"{valor / 1_000_000_000:.1f}") + " bi"
    if valor >= 1_000_000:
        return para_pt(f"{valor / 1_000_000:.1f}") + " mi"
    return para_pt(f"{valor:,.0f}")


def tipo_ativo(ticker: str) -> str:
    t = ticker.upper()
    if t.endswith("11.SA"):
        return "FII"
    if t.endswith(".SA"):
        return "Ação"
    if t.endswith("-USD"):
        return "Cripto"
    return "Ação internacional"


def tipo_ativo_descritivo(ticker: str) -> str:
    tipo = tipo_ativo(ticker)
    return {
        "FII": "Fundo imobiliário",
        "Ação": "Ação",
        "Cripto": "Criptomoeda",
        "Ação internacional": "Ação internacional",
    }.get(tipo, tipo)


def mercado_ativo(ticker: str) -> str:
    t = ticker.upper()
    if t.endswith(".SA"):
        return "Brasil"
    if t.endswith("-USD"):
        return "Global"
    return "Internacional"


# ============================================================
# BARRA LATERAL
# ============================================================
with st.sidebar:
    st.markdown(
        f"""
        <div class="brand-wrap">
            <div class="brand-logo">➤</div>
            <div>
                <p class="brand-title">{NOME_APP}</p>
                <p class="brand-sub">{TAGLINE}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pagina = st.radio(
        "Navegação",
        ["Análise de ativos", "Conteúdos educativos", "Sobre a Bússola"],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="sidebar-note">
            <div class="sidebar-note-icon">◇</div>
            <div>
                Ferramenta educacional.<br>
                Não é recomendação<br>
                de investimento.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# PÁGINA: ANÁLISE DE ATIVOS
# ============================================================
if pagina == "Análise de ativos":
    hc1, hc2 = st.columns([4.3, 1.2], vertical_alignment="top")

    with hc1:
        st.markdown('<h1 class="page-title">Análise de ativos</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="page-subtitle">Explore os dados. Entenda o contexto.</p>',
            unsafe_allow_html=True,
        )

    with hc2:
        st.markdown(
            """
            <div style="display:flex;justify-content:flex-end;padding-top:.15rem;">
                <span class="pill pill-green">ⓘ &nbsp; Ambiente demonstrativo</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    sc1, sc2 = st.columns([5.5, 1], gap="small")

    with sc1:
        ticker = st.text_input(
            "Ticker",
            value="MXRF11.SA",
            placeholder="Busque pelo nome ou ticker",
            label_visibility="collapsed",
        )
        st.markdown(
            '<div class="search-caption">Busque pelo nome ou ticker.</div>',
            unsafe_allow_html=True,
        )

    with sc2:
        analisar = st.button(
            "Analisar ativo  →",
            type="primary",
        )

    deve_renderizar = True

    if deve_renderizar:
        quote = None
        resultado = None
        erro_dados = None
        erro_ia = None

        try:
            with st.spinner("Buscando dados de mercado..."):
                quote = buscar_dados(ticker)
        except Exception as e:
            erro_dados = e

        if quote is not None:
            try:
                with st.spinner("IA analisando o ativo..."):
                    resultado = analisar_com_ia(ticker)
            except Exception as e:
                erro_ia = e

            # ---------------- Cabeçalho do ativo ----------------
            ac1, ac2 = st.columns([3.2, 2], vertical_alignment="bottom")
            with ac1:
                st.markdown(
                    f"""
                    <div style="display:flex;align-items:center;gap:.1rem;">
                        <h2 class="asset-title">{quote.ticker.replace(".SA","")}</h2>
                        <span class="pill pill-gray">{tipo_ativo(ticker)}</span>
                    </div>
                    <p class="asset-name">{quote.name}</p>
                    """,
                    unsafe_allow_html=True,
                )

            with ac2:
                st.markdown(
                    """
                    <div class="top-note">ⓘ <span>Dados: Yahoo Finance • Análise gerada por IA.</span></div>
                    """,
                    unsafe_allow_html=True,
                )

            # ---------------- Barra de métricas ----------------
            st.markdown(
                f"""
                <div class="card metric-bar">
                    <div class="metric-row">
                        <div class="metric-item">
                            <div class="metric-icon">◉</div>
                            <div>
                                <p class="metric-label">Preço de referência</p>
                                <p class="metric-value">{formatar_moeda(quote.current_price, quote.currency)}</p>
                            </div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-icon">◔</div>
                            <div>
                                <p class="metric-label">Valor de mercado</p>
                                <p class="metric-value">{formatar_valor_grande(quote.market_cap)}</p>
                            </div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-icon">▥</div>
                            <div>
                                <p class="metric-label">Setor</p>
                                <p class="metric-value">{quote.sector or "—"}</p>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ---------------- Painéis principais ----------------
            p1, p2 = st.columns([1.65, 1], gap="medium")

            with p1:
                st.markdown(
                    f"""
                    <div class="card panel">
                        <div class="panel-title-row">
                            <div class="panel-icon">▤</div>
                            <p class="card-title">Sobre o ativo</p>
                        </div>
                        <p class="card-sub">Informações básicas do ativo selecionado.</p>
                        <div class="info-table">
                            <div class="info-row">
                                <span class="info-label">Código</span>
                                <span class="info-value">{quote.ticker.replace(".SA","")}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Tipo</span>
                                <span class="info-value">{tipo_ativo_descritivo(ticker)}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Mercado</span>
                                <span class="info-value">{mercado_ativo(ticker)}</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with p2:
                if resultado is not None:
                    st.markdown(
                        f"""
                        <div class="card panel ai-panel">
                            <div class="panel-title-row">
                                <div class="panel-icon">✦</div>
                                <p class="card-title">Análise com IA</p>
                            </div>
                            <p class="card-sub">Análise do ativo com apoio de inteligência artificial.</p>
                            <div class="ai-content" style="align-items:flex-start;justify-content:flex-start;">
                                <div class="ai-summary">{resultado.executive_summary}</div>
                                <div class="verdict">◎ &nbsp; {resultado.final_verdict}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div class="card panel ai-panel">
                            <div class="panel-title-row">
                                <div class="panel-icon">✦</div>
                                <p class="card-title">Análise com IA</p>
                            </div>
                            <p class="card-sub">Análise do ativo com apoio de inteligência artificial.</p>
                            <div class="ai-content">
                                <div class="warning-icon">⚠</div>
                                <div class="unavailable-title">Análise indisponível</div>
                                <p class="unavailable-text">
                                    Não foi possível gerar a análise agora.<br>
                                    Os dados do ativo continuam disponíveis.
                                </p>
                                <div class="retry-like">⟳ &nbsp; Tentar novamente</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if erro_ia is not None:
                        with st.expander("Detalhes técnicos"):
                            st.exception(erro_ia)

            # ---------------- Pontos fortes e riscos ----------------
            if resultado is not None:
                st.markdown("<div style='height:.35rem'></div>", unsafe_allow_html=True)
                cf, cr = st.columns(2, gap="medium")

                with cf:
                    st.markdown(
                        '<p class="card-title" style="margin-bottom:.75rem;">Pontos fortes</p>',
                        unsafe_allow_html=True,
                    )
                    for ponto in resultado.strengths:
                        st.markdown(
                            f"<div class='card-forte'>✓ &nbsp; {ponto}</div>",
                            unsafe_allow_html=True,
                        )

                with cr:
                    st.markdown(
                        '<p class="card-title" style="margin-bottom:.75rem;">Riscos e alertas</p>',
                        unsafe_allow_html=True,
                    )
                    for risco in resultado.risks:
                        st.markdown(
                            f"<div class='card-risco'>⚠ &nbsp; {risco}</div>",
                            unsafe_allow_html=True,
                        )

        else:
            st.markdown(
                """
                <div class="card" style="margin-top:1.2rem;padding:2rem;text-align:center;">
                    <div class="warning-icon">⚠</div>
                    <div class="unavailable-title">Não foi possível carregar o ativo</div>
                    <p class="unavailable-text">
                        Verifique o ticker e tente novamente.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if erro_dados is not None:
                with st.expander("Detalhes técnicos"):
                    st.exception(erro_dados)

# ============================================================
# PÁGINA: CONTEÚDOS EDUCATIVOS
# ============================================================
elif pagina == "Conteúdos educativos":
    st.markdown('<h1 class="page-title">Conteúdos educativos</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Aprenda o básico antes de analisar.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card panel" style="min-height:auto;margin-bottom:1rem;">
            <p class="card-title">O que é um FII?</p>
            <p class="card-sub" style="margin-bottom:0;">
                Fundo Imobiliário: um "condomínio" de investidores que aplica em imóveis
                ou títulos do setor. Muitos distribuem rendimentos mensais aos cotistas.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card panel" style="min-height:auto;margin-bottom:1rem;">
            <p class="card-title">Ação vs. FII</p>
            <p class="card-sub" style="margin-bottom:0;">
                Ação é um pedaço de uma empresa; FII é um pedaço de uma carteira imobiliária.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card panel" style="min-height:auto;">
            <p class="card-title">O que a IA analisa aqui?</p>
            <p class="card-sub" style="margin-bottom:0;">
                Ela recebe os dados do ativo e produz um resumo com pontos fortes,
                riscos e um veredito educacional.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# PÁGINA: SOBRE A BÚSSOLA
# ============================================================
elif pagina == "Sobre a Bússola":
    st.markdown('<h1 class="page-title">Sobre a Bússola</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Clareza para suas decisões.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card panel" style="min-height:auto;margin-bottom:1rem;">
            <p class="card-title">Arquitetura</p>
            <p class="card-sub" style="margin-bottom:0;">
                Camada de dados (Yahoo Finance) → Camada de inteligência (IA via Groq) →
                Camada de apresentação (Streamlit), unidas por um agente orquestrador.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card panel" style="min-height:auto;margin-bottom:1rem;">
            <p class="card-title">Tecnologias</p>
            <p class="card-sub" style="margin-bottom:0;">
                Python • Orientação a Objetos • Pydantic • Streamlit • Groq •
                yfinance • Plotly
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card panel" style="min-height:auto;">
            <p class="card-title">Propósito</p>
            <p class="card-sub" style="margin-bottom:0;">
                Projeto de portfólio para demonstrar habilidades de análise de sistemas,
                integração de APIs e aplicação de IA com saída estruturada.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# RODAPÉ
# ============================================================
st.markdown(
    f"""
    <div class="footer-line">
        <div class="footer">
            <span>{NOME_APP} • Clareza para suas decisões.</span>
            <span>{dt.date.today().isoformat()}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)