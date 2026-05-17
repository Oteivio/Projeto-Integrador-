import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="BMW Global Sales Portal (2018-2025)",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "theme" not in st.session_state:
    st.session_state.theme = "Escuro"

if "pagina" not in st.session_state:
    st.session_state.pagina = "Gráficos"

COLOR_BMW_BLUE = "#1C69D4"
COLOR_BMW_GRAY = "#8E9AA6"

if st.session_state.theme == "Escuro":
    BG_COLOR = "#0A192F"
    TEXT_COLOR = "#E2E8F0"
    TITLE_COLOR = "#FFFFFF"
    SUBTITLE_COLOR = "#94A3B8"
    CARD_BG = "#172A45"
    CARD_BORDER = "none"
    CARD_TEXT = "#E2E8F0"
    CARD_TITLE_COLOR = "#FFFFFF"
    TECH_BG = "#0D1E36"
    TECH_BORDER = "none"
    TECH_TEXT = "#E2E8F0"
    HR_COLOR = "#1E293B"
    PLOTLY_TEMPLATE = "plotly_dark"
    PLOTLY_GRID = "#1E293B"
    PLOTLY_TICK = "#94A3B8"
else:
    BG_COLOR = "#FFFFFF"
    TEXT_COLOR = "#1E293B"
    TITLE_COLOR = "#0F172A"
    SUBTITLE_COLOR = "#475569"
    CARD_BG = "#F1F5F9"
    CARD_BORDER = "1px solid #E2E8F0"
    CARD_TEXT = "#0F172A"
    CARD_TITLE_COLOR = "#0F172A"
    TECH_BG = "#F8FAFC"
    TECH_BORDER = "1px solid #CBD5E1"
    TECH_TEXT = "#1E293B"
    HR_COLOR = "#E2E8F0"
    PLOTLY_TEMPLATE = "plotly"
    PLOTLY_GRID = "#E2E8F0"
    PLOTLY_TICK = "#475569"

st.markdown(f"""
    <style>
    /* Ocultar completamente a barra superior nativa (Deploy e Menu) */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}

    /* Ajuste de margem superior para compensar a perda do header */
    .block-container {{
        padding-top: 2rem !important;
    }}

    /* Configuração do fundo da página e iframes de componentes externos */
    .stApp {{
        background-color: {BG_COLOR} !important;
    }}

    iframe {{
        background-color: transparent !important;
    }}

    /* Customização Premium do painel lateral (Sidebar) */
    [data-testid="stSidebar"] {{
        background-color: {CARD_BG} !important;
        border-right: {CARD_BORDER} !important;
        min-width: 280px !important;
        max-width: 320px !important;
    }}

    /* Aplicar cor do texto geral de forma cirúrgica para não afetar inputs nativos - AMPLIADO PARA 1.25rem */
    .stMarkdown p, .stMarkdown span, .stWrite, p, li, span {{
        color: {TEXT_COLOR} !important;
        font-size: 1.25rem !important;
        line-height: 1.75 !important;
    }}

    /* Cabeçalhos e Títulos Principais */
    .main-title {{
        font-family: 'Outfit', 'Segoe UI', sans-serif;
        color: {TITLE_COLOR} !important;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.1rem;
    }}
    .subtitle {{
        font-family: 'Outfit', 'Segoe UI', sans-serif;
        color: {SUBTITLE_COLOR} !important;
        font-size: 1.25rem;
        margin-bottom: 0.5rem;
    }}

    /* Garantir que todos os títulos Markdown tenham a cor certa do tema e sejam GRANDES */
    h1 {{
        font-size: 2.5rem !important;
        color: {TITLE_COLOR} !important;
    }}
    h2 {{
        font-size: 2.0rem !important;
        color: {TITLE_COLOR} !important;
    }}
    h3 {{
        font-size: 1.6rem !important;
        color: {TITLE_COLOR} !important;
    }}
    h4 {{
        font-size: 1.35rem !important;
        color: {TITLE_COLOR} !important;
    }}

    [data-testid="stWidgetLabel"] p {{
        color: {TITLE_COLOR} !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }}

    /* Forçar contraste e TAMANHO nos rótulos de filtros e seletores */
    label {{
        color: {TITLE_COLOR} !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
    }}

    /* Aumentar fonte dos seletores (multiselect, selectbox) e garantir fundo/fonte adaptáveis ao Tema Escuro */
    div[data-baseweb="select"] > div {{
        background-color: {CARD_BG} !important;
        border: {CARD_BORDER} !important;
    }}
    div[data-baseweb="select"] span, div[data-baseweb="select"] input, div[data-baseweb="select"] div {{
        font-size: 1.2rem !important;
        color: {TEXT_COLOR} !important;
    }}
    /* Dropdown list items e Tags no Tema Escuro */
    ul[data-baseweb="menu"] {{
        background-color: {CARD_BG} !important;
    }}
    li[role="option"] {{
        background-color: {CARD_BG} !important;
        color: {TEXT_COLOR} !important;
    }}
    li[role="option"]:hover {{
        background-color: {COLOR_BMW_BLUE} !important;
        color: #FFFFFF !important;
    }}
    span[data-baseweb="tag"] {{
        background-color: {COLOR_BMW_BLUE} !important;
        color: #FFFFFF !important;
    }}

    /* Aumentar fonte dos sliders */
    div[data-testid="stSlider"] div {{
        font-size: 1.2rem !important;
    }}

    /* Aumentar fonte da tabela do dataframe */
    div[data-testid="stDataFrame"] * {{
        font-size: 1.15rem !important;
    }}

    /* Botões personalizados para contraste e visibilidade impecável */
    div.stButton > button {{
        background-color: {CARD_BG} !important;
        color: {TITLE_COLOR} !important;
        border: 2px solid #1C69D4 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }}

    div.stButton > button:hover {{
        background-color: #1C69D4 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 10px rgba(28, 105, 212, 0.4) !important;
    }}

    /* Estilização para o botão primário (página ativa) no menu lateral */
    [data-testid="stSidebar"] button[kind="primary"] {{
        background-color: #1C69D4 !important;
        color: #FFFFFF !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(28, 105, 212, 0.4) !important;
    }}

    /* Estilização para o botão secundário (páginas inativas) no menu lateral */
    [data-testid="stSidebar"] button[kind="secondary"] {{
        background-color: transparent !important;
        color: {TEXT_COLOR} !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border: 1px solid {HR_COLOR} !important;
    }}

    [data-testid="stSidebar"] button[kind="secondary"]:hover {{
        background-color: {HR_COLOR} !important;
        color: {TITLE_COLOR} !important;
        border-color: #1C69D4 !important;
    }}

    /* Cards de métricas principais do Dashboard */
    .metric-card {{
        background-color: {CARD_BG} !important;
        border: {CARD_BORDER} !important;
        border-left: 5px solid #1C69D4 !important;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}

    /* Textos editoriais de veículos ampliados para alta legibilidade */
    .editorial-text {{
        font-family: 'Outfit', 'Segoe UI', sans-serif !important;
        font-size: 1.25rem !important;
        line-height: 1.75 !important;
        color: {TEXT_COLOR} !important;
        margin-bottom: 1.25rem !important;
    }}
    .editorial-header {{
        font-family: 'Outfit', 'Segoe UI', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: {TITLE_COLOR} !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }}

    /* Customização das abas internas horizontais de modelos (st.tabs) - AMPLIADA PARA 1.35rem */
    div[data-testid="stTabBar"] button {{
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: {SUBTITLE_COLOR} !important;
        background-color: transparent !important;
        padding: 0.7rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }}

    div[data-testid="stTabBar"] button[aria-selected="true"] {{
        color: #1C69D4 !important;
        border-bottom-color: #1C69D4 !important;
        border-bottom-width: 3px !important;
    }}

    /* ----------------- CSS DO VISUALIZADOR DE FOTOS (CARROSSEL PREMIUM ANIMADO) ----------------- */
    .carousel-container {{
        position: relative;
        width: 100%;
        height: 480px;
        overflow: hidden;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.25);
        background-color: {BG_COLOR} !important;
        border: {CARD_BORDER} !important;
        margin-top: 1rem;
    }}

    .carousel-container input[type="radio"] {{
        display: none !important;
    }}

    .slides-wrapper {{
        display: flex;
        width: 300%;
        height: 100%;
        transition: transform 0.65s cubic-bezier(0.77, 0, 0.175, 1);
    }}

    .slide {{
        width: 33.333%;
        height: 100%;
    }}

    .slide img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        background-color: {BG_COLOR};
    }}

    .arrows {{
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 100%;
        display: none;
        justify-content: space-between;
        padding: 0 20px;
        box-sizing: border-box;
        pointer-events: none;
        z-index: 10;
    }}

    .prev-arrow, .next-arrow {{
        background-color: rgba(0, 0, 0, 0.65);
        color: #FFFFFF !important;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem !important;
        cursor: pointer;
        user-select: none;
        transition: all 0.3s ease;
        pointer-events: auto;
        z-index: 12;
    }}

    .prev-arrow:hover, .next-arrow:hover {{
        background-color: #1C69D4;
        color: #FFFFFF !important;
        transform: scale(1.12);
    }}

    .dots-wrapper {{
        position: absolute;
        bottom: 20px;
        width: 100%;
        display: flex;
        justify-content: center;
        gap: 10px;
        z-index: 15;
        pointer-events: none;
    }}

    .dot {{
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        pointer-events: auto;
        z-index: 16;
    }}

    /* Configuração de deslizamento das abas com base nos inputs de rádio */
    #slide-3-series-1:checked ~ .slides-wrapper,
    #slide-5-series-1:checked ~ .slides-wrapper,
    #slide-mini-1:checked ~ .slides-wrapper,
    #slide-x3-1:checked ~ .slides-wrapper,
    #slide-x5-1:checked ~ .slides-wrapper,
    #slide-x7-1:checked ~ .slides-wrapper,
    #slide-i4-1:checked ~ .slides-wrapper,
    #slide-ix-1:checked ~ .slides-wrapper {{
        transform: translateX(0);
    }}

    #slide-3-series-2:checked ~ .slides-wrapper,
    #slide-5-series-2:checked ~ .slides-wrapper,
    #slide-mini-2:checked ~ .slides-wrapper,
    #slide-x3-2:checked ~ .slides-wrapper,
    #slide-x5-2:checked ~ .slides-wrapper,
    #slide-x7-2:checked ~ .slides-wrapper,
    #slide-i4-2:checked ~ .slides-wrapper,
    #slide-ix-2:checked ~ .slides-wrapper {{
        transform: translateX(-33.333%);
    }}

    #slide-3-series-3:checked ~ .slides-wrapper,
    #slide-5-series-3:checked ~ .slides-wrapper,
    #slide-mini-3:checked ~ .slides-wrapper,
    #slide-x3-3:checked ~ .slides-wrapper,
    #slide-x5-3:checked ~ .slides-wrapper,
    #slide-x7-3:checked ~ .slides-wrapper,
    #slide-i4-3:checked ~ .slides-wrapper,
    #slide-ix-3:checked ~ .slides-wrapper {{
        transform: translateX(-66.666%);
    }}

    /* Mostrar as setas correspondentes de forma exclusiva */
    #slide-3-series-1:checked ~ .arrows-1, #slide-5-series-1:checked ~ .arrows-1, #slide-mini-1:checked ~ .arrows-1, #slide-x3-1:checked ~ .arrows-1, #slide-x5-1:checked ~ .arrows-1, #slide-x7-1:checked ~ .arrows-1, #slide-i4-1:checked ~ .arrows-1, #slide-ix-1:checked ~ .arrows-1 {{ display: flex; }}
    #slide-3-series-2:checked ~ .arrows-2, #slide-5-series-2:checked ~ .arrows-2, #slide-mini-2:checked ~ .arrows-2, #slide-x3-2:checked ~ .arrows-2, #slide-x5-2:checked ~ .arrows-2, #slide-x7-2:checked ~ .arrows-2, #slide-i4-2:checked ~ .arrows-2, #slide-ix-2:checked ~ .arrows-2 {{ display: flex; }}
    #slide-3-series-3:checked ~ .arrows-3, #slide-5-series-3:checked ~ .arrows-3, #slide-mini-3:checked ~ .arrows-3, #slide-x3-3:checked ~ .arrows-3, #slide-x5-3:checked ~ .arrows-3, #slide-x7-3:checked ~ .arrows-3, #slide-i4-3:checked ~ .arrows-3, #slide-ix-3:checked ~ .arrows-3 {{ display: flex; }}

    /* Destacar a bolinha selecionada com efeito pill esticado */
    #slide-3-series-1:checked ~ .dots-wrapper .dot:nth-child(1), #slide-5-series-1:checked ~ .dots-wrapper .dot:nth-child(1), #slide-mini-1:checked ~ .dots-wrapper .dot:nth-child(1), #slide-x3-1:checked ~ .dots-wrapper .dot:nth-child(1), #slide-x5-1:checked ~ .dots-wrapper .dot:nth-child(1), #slide-x7-1:checked ~ .dots-wrapper .dot:nth-child(1), #slide-i4-1:checked ~ .dots-wrapper .dot:nth-child(1), #slide-ix-1:checked ~ .dots-wrapper .dot:nth-child(1) {{ background-color: #1C69D4; width: 32px; border-radius: 6px; }}
    #slide-3-series-2:checked ~ .dots-wrapper .dot:nth-child(2), #slide-5-series-2:checked ~ .dots-wrapper .dot:nth-child(2), #slide-mini-2:checked ~ .dots-wrapper .dot:nth-child(2), #slide-x3-2:checked ~ .dots-wrapper .dot:nth-child(2), #slide-x5-2:checked ~ .dots-wrapper .dot:nth-child(2), #slide-x7-2:checked ~ .dots-wrapper .dot:nth-child(2), #slide-i4-2:checked ~ .dots-wrapper .dot:nth-child(2), #slide-ix-2:checked ~ .dots-wrapper .dot:nth-child(2) {{ background-color: #1C69D4; width: 32px; border-radius: 6px; }}
    #slide-3-series-3:checked ~ .dots-wrapper .dot:nth-child(3), #slide-5-series-3:checked ~ .dots-wrapper .dot:nth-child(3), #slide-mini-3:checked ~ .dots-wrapper .dot:nth-child(3), #slide-x3-3:checked ~ .dots-wrapper .dot:nth-child(3), #slide-x5-3:checked ~ .dots-wrapper .dot:nth-child(3), #slide-x7-3:checked ~ .dots-wrapper .dot:nth-child(3), #slide-i4-3:checked ~ .dots-wrapper .dot:nth-child(3), #slide-ix-3:checked ~ .dots-wrapper .dot:nth-child(3) {{ background-color: #1C69D4; width: 32px; border-radius: 6px; }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="collapsedSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stSidebar"] {
        display: none !important;
    }
    /* Expandir container principal */
    .block-container {
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_clean = os.path.join(caminho_atual, "..", "data", "bmw_global_sales_2018_2025_cleaned.csv")
    caminho_raw = os.path.join(caminho_atual, "..", "data", "bmw_global_sales_2018_2025.csv")

    if os.path.exists(caminho_clean):
        df = pd.read_csv(caminho_clean)
    elif os.path.exists(caminho_raw):
        df = pd.read_csv(caminho_raw)
        df.drop_duplicates(inplace=True)
    else:
        st.error("Base de dados da BMW nao encontrada na pasta `/data`!")
        st.stop()
    return df

df = get_data()

def renderizar_graficos(df_filtrado):
    st.markdown("<br>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        df_evolucao = df_filtrado.copy()
        df_evolucao['Periodo'] = df_evolucao['Year'].astype(str) + '-' + df_evolucao['Month'].astype(str).str.zfill(2)
        df_evolucao = df_evolucao.groupby(['Periodo', 'Region'])['Revenue_EUR'].sum().reset_index().sort_values('Periodo')

        fig1 = px.line(
            df_evolucao,
            x="Periodo",
            y="Revenue_EUR",
            color="Region",
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Bold,
            template=PLOTLY_TEMPLATE
        )
        fig1.update_traces(
            hovertemplate="<b>Regiao:</b> %{fullData.name}<br>" +
                          "<b>Periodo:</b> %{x}<br>" +
                          "<b>Receita Total:</b> € %{y:,.0f}<extra></extra>"
        )
        fig1.update_layout(
            title=dict(
                text="Evolucao Mensal da Receita por Regiao (€)",
                font=dict(color=TITLE_COLOR, size=20)
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Periodo (Ano-Mes)",
            yaxis_title="Receita Total (€)",
            legend_title="Mercados/Regioes",
            legend=dict(
                font=dict(color=TEXT_COLOR, size=12)
            ),
            hovermode="closest"
        )
        fig1.update_xaxes(
            title_font=dict(color=TITLE_COLOR, size=15),
            tickfont=dict(color=PLOTLY_TICK, size=13),
            showspikes=True,
            spikemode="marker",
            spikesnap="cursor",
            fixedrange=True,
            gridcolor=PLOTLY_GRID,
            tickcolor=PLOTLY_TICK
        )
        fig1.update_yaxes(
            title_font=dict(color=TITLE_COLOR, size=15),
            tickfont=dict(color=PLOTLY_TICK, size=13),
            showspikes=True,
            spikemode="marker",
            spikesnap="cursor",
            fixedrange=True,
            gridcolor=PLOTLY_GRID,
            tickcolor=PLOTLY_TICK
        )
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    with chart_col2:

        df_temporal = df_filtrado.copy()
        df_temporal['Periodo'] = df_temporal['Year'].astype(str) + '-' + df_temporal['Month'].astype(str).str.zfill(2)
        df_temporal = df_temporal.groupby('Periodo').agg({
            'Fuel_Price_Index': 'mean',
            'Units_Sold': 'sum'
        }).reset_index().sort_values('Periodo')

        fig2 = make_subplots(specs=[[{"secondary_y": True}]])

        fig2.add_trace(
            go.Scatter(
                x=df_temporal['Periodo'],
                y=df_temporal['Units_Sold'],
                name="Unidades Vendidas",
                mode="lines",
                line=dict(color=COLOR_BMW_BLUE, width=3),
                hovertemplate="<b>Periodo:</b> %{x}<br><b>Vendas:</b> %{y:,.0f} unidades<extra></extra>"
            ),
            secondary_y=True
        )

        fig2.add_trace(
            go.Scatter(
                x=df_temporal['Periodo'],
                y=df_temporal['Fuel_Price_Index'],
                name="Indice Preço Combustivel",
                mode="lines",
                line=dict(color="#EF4444", width=3),
                hovertemplate="<b>Periodo:</b> %{x}<br><b>Indice Combustivel:</b> %{y:.3f}<extra></extra>"
            ),
            secondary_y=False
        )

        fig2.update_layout(
            title=dict(
                text="Tendencia Historica: Preco do Combustivel vs. Veiculos Vendidos",
                font=dict(color=TITLE_COLOR, size=20)
            ),
            template=PLOTLY_TEMPLATE,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Linha do Tempo (Ano-Mes)",
                title_font=dict(color=TITLE_COLOR, size=15),
                tickfont=dict(color=PLOTLY_TICK, size=13),
                showgrid=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color=TEXT_COLOR, size=12)
            ),
            hovermode="closest"
        )
        fig2.update_xaxes(
            showspikes=True,
            spikemode="marker",
            spikesnap="cursor",
            fixedrange=True,
            tickcolor=PLOTLY_TICK
        )
        fig2.update_yaxes(
            showspikes=True,
            spikemode="marker",
            spikesnap="cursor",
            fixedrange=True,
            secondary_y=False,
            tickcolor=PLOTLY_TICK
        )
        fig2.update_yaxes(
            showspikes=True,
            spikemode="marker",
            spikesnap="cursor",
            fixedrange=True,
            secondary_y=True,
            tickcolor=PLOTLY_TICK
        )
        fig2.update_yaxes(title_text="Indice de Preco do Combustivel", title_font=dict(color=TITLE_COLOR, size=15), tickfont=dict(color=PLOTLY_TICK, size=13), secondary_y=False, showgrid=True, gridcolor=PLOTLY_GRID)
        fig2.update_yaxes(title_text="Veiculos Vendidos (Unidades)", title_font=dict(color=TITLE_COLOR, size=15), tickfont=dict(color=PLOTLY_TICK, size=13), secondary_y=True, showgrid=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

def renderizar_tabela(df_filtrado):
    st.markdown("### Tabela Comparativa de Registros Filtrados")
    st.markdown("Use a tabela abaixo para inspecionar, ordenar e pesquisar registros específicos:")

    df_exibicao = df_filtrado.rename(columns={
        "Year": "Ano",
        "Month": "Mês",
        "Region": "Região",
        "Model": "Modelo BMW",
        "Units_Sold": "Unidades Vendidas",
        "Avg_Price_EUR": "Preço Médio (€)",
        "Revenue_EUR": "Faturamento (€)",
        "BEV_Share": "Fração BEV (Elétricos)",
        "Premium_Share": "Premium Share",
        "GDP_Growth": "Crescimento PIB",
        "Fuel_Price_Index": "Índice Preço Combustível",
        "is_high_electric": "Fração Alta de Elétrico"
    })

    def formatar_moeda_br(val):
        if pd.isna(val):
            return ""
        formatted = f"{val:,.2f}"
        return "€ " + formatted.replace(",", "v").replace(".", ",").replace("v", ".")

    df_exibicao["Preço Médio (€)"] = df_exibicao["Preço Médio (€)"].apply(formatar_moeda_br)
    df_exibicao["Faturamento (€)"] = df_exibicao["Faturamento (€)"].apply(formatar_moeda_br)

    df_estilizado = df_exibicao.style.set_properties(**{
        'background-color': CARD_BG,
        'color': TEXT_COLOR,
        'border-color': HR_COLOR
    })

    st.dataframe(df_estilizado, use_container_width=True)

col_header_title, col_header_toggle = st.columns([8.5, 1.5], vertical_alignment="center")

with col_header_title:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-bottom: 0;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg" width="60" style="margin-right: 15px;">
            <h1 class="main-title" style="margin-top: 0; margin-bottom: 0;">BMW Global Sales Portal</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_header_toggle:
    rotulo_botao = "Modo Claro" if st.session_state.theme == "Escuro" else "Modo Escuro"

    if st.button(f"🌓 {rotulo_botao}", use_container_width=True):
        st.session_state.theme = "Claro" if st.session_state.theme == "Escuro" else "Escuro"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

menu_selecionado = option_menu(
    menu_title=None,
    options=["Dashboard de Gráficos", "Catálogo de Veículos"],
    icons=["bar-chart-fill", "car-front-fill"],
    default_index=0 if st.session_state.pagina == "Gráficos" else 1,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important",
            "background-color": CARD_BG,
            "margin": "0 auto !important",
            "margin-bottom": "2rem !important",
            "border": f"1px solid {HR_COLOR}",
            "border-radius": "0px",
            "width": "100% !important",
            "max-width": "100% !important",
            "display": "flex"
        },
        "icon": {"color": "#1C69D4", "font-size": "20px"},
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#e2e8f0" if st.session_state.theme == "Claro" else "#1e293b",
            "color": TEXT_COLOR,
            "border-radius": "10px",
            "font-family": "Outfit",
            "font-weight": "600",
            "padding": "15px"
        },
        "nav-link-selected": {
            "background-color": "#1C69D4",
            "color": "white",
            "font-weight": "800",
            "box-shadow": "0 4px 10px rgba(28, 105, 212, 0.4)"
        },
    }
)

if menu_selecionado == "Dashboard de Gráficos" and st.session_state.pagina != "Gráficos":
    st.session_state.pagina = "Gráficos"
    st.rerun()
elif menu_selecionado == "Catálogo de Veículos" and st.session_state.pagina != "Veículos":
    st.session_state.pagina = "Veículos"
    st.rerun()

if st.session_state.pagina == "Gráficos":
    st.markdown(f'<p class="subtitle" style="margin-top: 0; color: {SUBTITLE_COLOR};">Indicadores Comerciais, Desempenho Regional e Tendências Macroeconômicas</p>', unsafe_allow_html=True)
else:
    st.markdown(f'<p class="subtitle" style="margin-top: 0; color: {SUBTITLE_COLOR};">Especificações de Engenharia, Motorização e Dados de Vendas por Modelo</p>', unsafe_allow_html=True)

st.markdown("---")

if st.session_state.pagina == "Gráficos":

    container_kpis = st.container()
    container_graficos = st.container()

    st.markdown("---")
    st.markdown("### Filtros Rapidos de Analise")
    filtro_col1, filtro_col2, filtro_col3 = st.columns(3)

    with filtro_col1:
        anos = sorted(df['Year'].unique())
        ano_min, ano_max = st.select_slider(
            "Selecione o Intervalo de Anos:",
            options=anos,
            value=(min(anos), max(anos))
        )

    with filtro_col2:
        regioes = sorted(df['Region'].unique())
        regioes_selecionadas = st.multiselect(
            "Selecione as Regioes:",
            options=regioes,
            default=regioes
        )

    with filtro_col3:
        modelos = sorted(df['Model'].unique())
        modelos_selecionados = st.multiselect(
            "Selecione os Modelos da BMW:",
            options=modelos,
            default=modelos
        )

    df_filtrado = df[
        (df['Year'] >= ano_min) & (df['Year'] <= ano_max) &
        (df['Region'].isin(regioes_selecionadas)) &
        (df['Model'].isin(modelos_selecionados))
    ]

    if df_filtrado.empty:
        with container_kpis:
            st.warning("Nenhum registro encontrado para a combinacao de filtros selecionada. Ajuste as opcoes de filtros abaixo.")
    else:

        with container_kpis:
            col1, col2, col3, col4 = st.columns(4)

        with col1:
            receita_total = df_filtrado['Revenue_EUR'].sum()
            st.markdown(
                f"""
                <div class="metric-card">
                    <span style="color: {COLOR_BMW_GRAY}; font-size: 1.2rem; font-weight: 700; text-transform: uppercase; font-family: Outfit;">FATURAMENTO TOTAL</span><br>
                    <span style="color: {CARD_TITLE_COLOR}; font-size: 2.3rem; font-weight: 800; font-family: Outfit;">€ {receita_total:,.0f}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            total_vendas = df_filtrado['Units_Sold'].sum()
            st.markdown(
                f"""
                <div class="metric-card">
                    <span style="color: {COLOR_BMW_GRAY}; font-size: 1.2rem; font-weight: 700; text-transform: uppercase; font-family: Outfit;">UNIDADES VENDIDAS</span><br>
                    <span style="color: {CARD_TITLE_COLOR}; font-size: 2.3rem; font-weight: 800; font-family: Outfit;">{total_vendas:,.0f} unds</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            preco_medio = df_filtrado['Avg_Price_EUR'].mean()
            st.markdown(
                f"""
                <div class="metric-card">
                    <span style="color: {COLOR_BMW_GRAY}; font-size: 1.2rem; font-weight: 700; text-transform: uppercase; font-family: Outfit;">PREÇO MÉDIO PRATICADO</span><br>
                    <span style="color: {CARD_TITLE_COLOR}; font-size: 2.3rem; font-weight: 800; font-family: Outfit;">€ {preco_medio:,.2f}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            bev_share_medio = df_filtrado['BEV_Share'].mean() * 100
            st.markdown(
                f"""
                <div class="metric-card">
                    <span style="color: {COLOR_BMW_GRAY}; font-size: 1.2rem; font-weight: 700; text-transform: uppercase; font-family: Outfit;">PARTICIPAÇÃO ELÉTRICOS (BEV)</span><br>
                    <span style="color: {CARD_TITLE_COLOR}; font-size: 2.3rem; font-weight: 800; font-family: Outfit;">{bev_share_medio:.2f}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with container_graficos:
            renderizar_graficos(df_filtrado)

        renderizar_tabela(df_filtrado)

else:

    modelos_disponiveis = sorted(df['Model'].unique())

    abas = st.tabs(modelos_disponiveis)

    detalhes_carros = {
        "3 Series": {
            "slogan": "O sedan esportivo definitivo da engenharia alemã.",
            "descricao": "A Série 3 da BMW representa o coração histórico e a alma da marca bávara. Consagrado globalmente como o benchmark absoluto em dinâmica de direção, é famoso por sua distribuição de peso perfeita de 50:50, direção ultra comunicativa e tração traseira que proporciona o clássico prazer de dirigir. Combina perfeitamente presença executiva com vigor mecânico de alta classe.",
            "categoria": "Sedan Esportivo Premium",
            "diferencial": "Legado de chassi com distribuição ideal de peso (50:50) e dirigibilidade lendária.",
            "motorizacao": "Motores BMW TwinPower Turbo potentes e eficientes transmissões Steptronic de 8 marchas.",
            "futuro": "Forte transição híbrida plug-in (PHEV) de alta performance que combina o melhor de dois mundos.",
            "imagens": [
                "https://images.unsplash.com/photo-1603386329225-868f9b1ee6c9?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&q=80&w=800"
            ]
        },
        "5 Series": {
            "slogan": "O sedan de negócios executivo com presença executiva marcante.",
            "descricao": "A Série 5 define o que significa viajar com máximo conforto acústico e sofisticação luxuosa nas famosas Autobahns alemãs. É o sedan de negócios preferido por líderes ao redor do mundo, apresentando inovações tecnológicas revolucionárias como o BMW Live Cockpit Professional com telas integradas curvas e sistemas avançados de assistência autônoma de nível 2+.",
            "categoria": "Sedan Executivo de Luxo / Business",
            "diferencial": "Excepcional isolamento acústico de cabine e dinâmica refinada para longas viagens rodoviárias.",
            "motorizacao": "Mix equilibrado de propulsores turbodiesel e turbogasolina de alta cilindrada.",
            "futuro": "Ingresso no mercado de híbridos inteligentes e total eletrificação sob a marca i5.",
            "imagens": [
                "https://images.unsplash.com/photo-1617531653332-bd46c24f2068?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&q=80&w=800"
            ]
        },
        "MINI": {
            "slogan": "O carisma icônico e a agilidade 'Go-Kart Feeling' sobre rodas.",
            "descricao": "A MINI, marca de herança britânica sob o comando do BMW Group, é sinônimo de personalidade forte, design retrô-moderno atemporal e um comportamento dinâmico incomparável conhecido como 'Go-Kart Feeling' (a sensação de dirigir um kart super ágil). É a escolha ideal para motoristas urbanos exigentes que priorizam estilo marcante, aproveitamento de espaço inteligente e manobrabilidade cirúrgica nas curvas.",
            "categoria": "Compacto Premium / Urbano Esportivo",
            "diferencial": "Direção direta ultra ágil ('Go-Kart Feeling') e design marcante de personalidade britânica clássica.",
            "motorizacao": "Motores turbo compactos TwinPower Turbo extremamente elásticos e de alta diversão.",
            "futuro": "Rápida transição para eletrificação completa sob a nova geração de modelos elétricos MINI Cooper SE.",
            "imagens": [
                "https://images.pexels.com/photos/3972239/pexels-photo-3972239.jpeg?auto=compress&cs=tinysrgb&w=800",
                "https://images.pexels.com/photos/2589409/pexels-photo-2589409.jpeg?auto=compress&cs=tinysrgb&w=800",
                "https://images.unsplash.com/photo-1611016186353-9af58c69a533?auto=format&fit=crop&q=80&w=800"
            ]
        },
        "X3": {
            "slogan": "Versatilidade aventureira de luxo em formato compacto-médio.",
            "descricao": "O BMW X3 foi um dos pioneiros da categoria SUV de luxo médio (chamado pela marca de SAV - Sports Activity Vehicle). Destina-se a famílias dinâmicas e aventureiros que exigem a tração integral inteligente xDrive de alta resposta, aliada a um amplo porta-malas flexível e cockpit moderno de alta conectividade para suportar qualquer viagem com conforto premium.",
            "categoria": "SUV Premium / SAV de Médio Porte",
            "diferencial": "Tração integral inteligente xDrive de série nas motorizações superiores, gerando estabilidade inabalável.",
            "motorizacao": "Propulsores altamente elásticos de 4 cilindros TwinPower Turbo de baixíssima vibração.",
            "futuro": "Versões eletrificadas e compatibilidade total com sistemas de recuperação de energia de frenagem.",
            "imagens": [
                "https://images.unsplash.com/photo-1605558230459-a522ecd3b5ad?auto=format&fit=crop&q=80&w=800",
                "https://images.pexels.com/photos/116675/pexels-photo-116675.jpeg?auto=compress&cs=tinysrgb&w=800",
                "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&q=80&w=800"
            ]
        },
        "X5": {
            "slogan": "O SUV grande de luxo supremo e referência indiscutível da categoria.",
            "descricao": "O lendário BMW X5 é o fundador do segmento SAV e continua definindo o patamar máximo de imponência e refinamento. Com suspensão a ar adaptativa nos dois eixos, interior com acabamentos primorosos em cristal facetado 'CraftedClarity' e amplo espaço interno, ele é a representação física de prestígio, poder de tração e excelência mecânica em qualquer tipo de terreno.",
            "categoria": "SUV Premium Grande de Alto Luxo",
            "diferencial": "Suspensão pneumática auto-nivelante e materiais de altíssima qualidade com acabamento feito à mão.",
            "motorizacao": "Família de potentes motores de 6 cilindros em linha e impressionantes motores V8 biturbo nas variantes M.",
            "futuro": "Destaque absoluto no mercado global com motorizações Híbridas Plug-in (PHEV) de grande autonomia.",
            "imagens": [
                "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&q=80&w=800",
                "https://images.pexels.com/photos/3729464/pexels-photo-3729464.jpeg?auto=compress&cs=tinysrgb&w=800",
                "https://images.pexels.com/photos/1592384/pexels-photo-1592384.jpeg?auto=compress&cs=tinysrgb&w=800"
            ]
        },
        "X7": {
            "slogan": "O maior, mais imponente e luxuoso SAV da história da BMW.",
            "descricao": "O BMW X7 é o ápice absoluto do luxo familiar em grande escala do grupo. Projetado para transportar com folga até 7 ocupantes em confortáveis poltronas individuais aquecidas de couro Merino macio, ele mescla a imponência monumental de um SUV de grande porte com a elegância aristocrática e tecnológica de um sedan Série 7. Oferece climatização independente em 5 zonas e teto solar Sky Lounge.",
            "categoria": "SUV Grande de Altíssimo Luxo (Full-Size SAV)",
            "diferencial": "Interior majestic de 3 fileiras, poltronas executivas capitonadas e suspensão pneumática active adaptável.",
            "motorizacao": "Soberbos propulsores de 6 cilindros inline e monstruosos motores V8 turbinados de suavidade impecável.",
            "futuro": "Inclusão de sistemas híbridos leves (MHEV) de 48V para rodagem macia e baixas emissões urbanas.",
            "imagens": [
                "https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?auto=format&fit=crop&q=80&w=800",
                "https://images.pexels.com/photos/2365572/pexels-photo-2365572.jpeg?auto=compress&cs=tinysrgb&w=800",
                "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&q=80&w=800"
            ]
        },
        "i4": {
            "slogan": "Design dinâmico Gran Coupé adaptado à era da eletrificação total.",
            "descricao": "O BMW i4 é um cupê de 4 portas 100% elétrico que prova que a esportividade clássica da marca permanece viva na era da bateria. Ele entrega torque instantâneo brutal que cola os ocupantes ao banco de forma linear e conta com o design interior curvo futurista da BMW, acompanhado da trilha sonora exclusiva 'BMW IconicSounds Electric' assinada pelo premiado compositor de cinema Hans Zimmer.",
            "categoria": "Gran Coupé 100% Elétrico (BEV)",
            "diferencial": "Silêncio absoluto na rodagem com aceleração esportiva agressiva de zero emissões locais.",
            "motorizacao": "Motores síncronos elétricos de quinta geração BMW eDrive instalados diretamente nos eixos traseiro/dianteiro.",
            "futuro": "O futuro elétrico da esportividade de volume, com baterias de recarga rápida ultra-otimizadas.",
            "imagens": [
                "https://images.pexels.com/photos/1805053/pexels-photo-1805053.jpeg?auto=compress&cs=tinysrgb&w=800",
                "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&q=80&w=800",
                "https://images.pexels.com/photos/244553/pexels-photo-244553.jpeg?auto=compress&cs=tinysrgb&w=800"
            ]
        },
        "iX": {
            "slogan": "O manifesto futurista e tecnológico da sustentabilidade móvel.",
            "descricao": "Construído sobre uma inovadora estrutura espacial (Spaceframe) de alumínio reforçada com gaiola de fibra de carbono, o BMW iX é o ápice da inovação. Traz a filosofia de design 'Shy Tech' (tecnologia oculta que só aparece quando necessária), grade frontal com propriedades regenerativas autoreparáveis a calor, e teto solar eletrocrômico panorâmico de cristal líquido.",
            "categoria": "SUV Tecnológico Premium 100% Elétrico",
            "diferencial": "Chassi de polímero reforçado com fibra de carbono (CFRP) e grade autorregenerativa com inteligência de sensores.",
            "motorizacao": "Tração integral elétrica gerada por dois motores síncronos e eDrive de altíssima eficiência global.",
            "futuro": "O veículo conceito de vanguarda que antecipa o design futurista, digitalização e reciclabilidade de toda a BMW.",
            "imagens": [
                "https://images.pexels.com/photos/1402787/pexels-photo-1402787.jpeg?auto=compress&cs=tinysrgb&w=800",
                "https://images.pexels.com/photos/3311574/pexels-photo-3311574.jpeg?auto=compress&cs=tinysrgb&w=800",
                "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=800"
            ]
        }
    }

    for aba, modelo_selecionado in zip(abas, modelos_disponiveis):
        with aba:
            df_modelo = df[df['Model'] == modelo_selecionado]
            vendas_totais = df_modelo['Units_Sold'].sum()
            receita_total = df_modelo['Revenue_EUR'].sum()
            preco_medio = df_modelo['Avg_Price_EUR'].mean()
            bev_share_modelo = df_modelo['BEV_Share'].mean() * 100
            regioes = sorted(df_modelo['Region'].unique())

            car_info = detalhes_carros.get(modelo_selecionado, {
                "slogan": "O autêntico Prazer de Dirigir.",
                "descricao": f"O modelo BMW {modelo_selecionado} entrega o máximo refinamento, engenharia bávara de alto nível e dinâmica impecável nas ruas e estradas.",
                "categoria": "Veículo de Alto Padrão BMW",
                "diferencial": "Padrão de manufatura alemão e chassi com acerto esportivo equilibrado.",
                "motorizacao": "Propulsão de alto rendimento com conectividade multimídia integrada.",
                "futuro": "Foco na eficiência energética global e materiais reciclados de baixo impacto.",
                "imagens": [
                    "https://images.unsplash.com/photo-1603386329225-868f9b1ee6c9?auto=format&fit=crop&q=80&w=800",
                    "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&q=80&w=800",
                    "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&q=80&w=800"
                ]
            })

            st.markdown(f"### BMW {modelo_selecionado}")
            st.markdown(f"*{car_info['slogan']}*")
            st.markdown("<br>", unsafe_allow_html=True)

            col_info1, col_info2 = st.columns([1, 1])

            with col_info1:

                st.markdown(f'<div class="editorial-header">Engenharia, Conceito e Dinâmica</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="editorial-text">{car_info["descricao"]}</div>', unsafe_allow_html=True)

                st.markdown(f'<div class="editorial-header">Motorização e Câmbio</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="editorial-text">{car_info["motorizacao"]}</div>', unsafe_allow_html=True)

            with col_info2:
                st.markdown(f'<div class="editorial-header">Transição Energética e Futuro</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="editorial-text">{car_info["futuro"]}</div>', unsafe_allow_html=True)

                st.markdown(f'<div class="editorial-header">Diferencial de Chassi e Estrutura</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="editorial-text">{car_info["diferencial"]}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div style="background-color: {CARD_BG}; padding: 2rem; border-radius: 12px; border-left: 5px solid {COLOR_BMW_BLUE}; border: {CARD_BORDER};">
                    <span style="color: {COLOR_BMW_GRAY}; font-size: 1.25rem; font-weight: bold; text-transform: uppercase; font-family: Outfit;">DADOS CONSOLIDADOS DO DATASET (2018-2025):</span><br><br>
                    <span style="font-size: 1.25rem; color: {TEXT_COLOR}; font-family: Outfit; line-height: 1.8;">
                        <b>Categoria Comercial:</b> {car_info['categoria']}<br>
                        <b>Faturamento Acumulado:</b> € {receita_total:,.0f}<br>
                        <b>Unidades Vendidas:</b> {vendas_totais:,.0f} unidades<br>
                        <b>Preço Praticado Médio:</b> € {preco_medio:,.2f}<br>
                        <b>Presença Regional:</b> {', '.join(regioes)}<br>
                        <b>Fração Média BEV (Elétricos):</b> {bev_share_modelo:.2f}%
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: {SUBTITLE_COLOR}; font-size: 1.1rem;'>"
    "Dashboard desenvolvido para entrega acadêmica do Projeto Integrador de Análise de Dados. "
    "Fabricante de dados de referência: BMW Group Global Historical Datasets (2018-2025)."
    "</p>",
    unsafe_allow_html=True
)
