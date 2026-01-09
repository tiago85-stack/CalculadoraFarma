import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Farmácia",
    page_icon="💊",
    layout="centered"
)

# --- ESTILIZAÇÃO (Botão e Métricas) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; margin-top: 15px; font-weight: bold; font-size: 18px; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #0066cc; }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS (Com Princípio Ativo) ---
medicamentos = {
    "Exodus / Lexapro (Escitalopram)":      {"gotas_ml": 20, "frasco_padrao": 15},
    "Daforin (Fluoxetina)":                 {"gotas_ml": 20, "frasco_padrao": 20},
    "Tramal (Tramadol)":                    {"gotas_ml": 40, "frasco_padrao": 10},
    "Lexotan (Bromazepam)":                 {"gotas_ml": 25, "frasco_padrao": 20},
    "Rivotril (Clonazepam)":                {"gotas_ml": 25, "frasco_padrao": 20},
    "Haldol (Haloperidol)":                 {"gotas_ml": 20, "frasco_padrao": 30},
    "Amplictil (Clorpromazina)":            {"gotas_ml": 40, "frasco_padrao": 20},
    "Gardenal (Fenobarbital)":              {"gotas_ml": 40, "frasco_padrao": 20},
    "Neozine (Levomepromazina)":            {"gotas_ml": 40, "frasco_padrao": 20},
    "Neuleptil (Periciazina)":              {"gotas_ml": 40, "frasco_padrao": 20},
}

# --- TÍTULO ---
st.title("💊 Calculadora de Dispensação")
st.markdown("---")

# --- 1. SELEÇÃO DO MEDICAMENTO ---
st.subheader("1. Medicamento")

nome_escolhido = st.selectbox(
    "Selecione o medicamento:",
    options=medicamentos.keys()
)
dados_med = medicamentos[nome_escolhido]

# Mostra o gotejamento apenas para confirmação visual
st.caption(f"ℹ️ Parâmetro de Bula: **{dados_med['gotas_ml']} gotas/mL**")

st.markdown("---")

# --- 2. VOLUME DO FRASCO (EDITÁVEL) ---
st.subheader("2. Volume do Frasco")

# Aqui está a mudança: Apenas um campo simples.
# Ele já vem com o valor padrão, mas você pode alterar se for Genérico.
tamanho_frasco = st.number_input(
    "Volume do frasco (mL):",
    min_value=1.0,
    value=float(dados_med['frasco_padrao']), # Traz o valor do banco
    step=1.0,
    format="%.1f",
    help="O valor vem preenchido com o padrão, mas você pode alterar para Genéricos."
)

st.markdown("---")

# --- 3. RECEITA MÉDICA ---
st.subheader("3. Posologia")

c1, c2 = st.columns(2)
with c1:
    gotas_por_dia = st.number_input("Gotas por Dia:", min_value=1, value=10)
with c2:
    dias_tratamento = st.number_input("Dias de Tratamento:", min_value=1, value=30)

# Alerta de legislação
if dias_tratamento > 60:
    st.error(f"⚠️ **Atenção:** {dias_tratamento} dias excede o limite de 60 dias.")

# --- CÁLCULO ---
if st.button("CALCULAR QUANTIDADE", type="primary"):
    
    # Lógica
    total_gotas = gotas_por_dia * dias_tratamento
    ml_necessarios = total_gotas / dados_med['
