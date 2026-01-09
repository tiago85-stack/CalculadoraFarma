import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Farmácia",
    page_icon="💊",
    layout="centered"
)

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; margin-top: 15px; font-weight: bold; font-size: 18px; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #0066cc; }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS (Princípio Ativo + Dados do PDF) ---
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

# --- 1. MEDICAMENTO ---
st.subheader("1. Medicamento")

nome_escolhido = st.selectbox(
    "Selecione o medicamento:",
    options=medicamentos.keys()
)
dados_med = medicamentos[nome_escolhido]

# Mostra o gotejamento informativo
st.caption(f"ℹ️ Bula: **{dados_med['gotas_ml']} gotas/mL**")

st.markdown("---")

# --- 2. VOLUME DO FRASCO (Livre para edição) ---
st.subheader("2. Volume do Frasco")

tamanho_frasco = st.number_input(
    "Volume do frasco (mL):",
    min_value=1.0,
    value=float(dados_med['frasco_padrao']), # Vem do banco, mas você edita se quiser
    step=1.0,
    format="%.1f",
    help="Altere este valor se estiver vendendo um genérico com volume diferente."
)

st.markdown("---")

# --- 3. POSOLOGIA ---
st.subheader("3. Receita Médica")

c1, c2 = st.columns(2)
with c1:
    gotas_por_dia = st.number_input("Gotas por Dia:", min_value=1, value=10)
with c2:
    dias_tratamento = st.number_input("Dias de Tratamento:", min_value=1, value=30)

if dias_tratamento > 60:
    st.error(f"⚠️ **Atenção:** {dias_tratamento} dias excede o limite de 60 dias.")

# --- CÁLCULO E LÓGICA ---
if st.button("CALCULAR QUANTIDADE", type="primary"):
    
    # 1. Total necessário
    total_gotas = gotas_por_dia * dias_tratamento
    ml_necessarios = total_gotas / dados_med['gotas_ml']
    
    # 2. Quantidade de caixas
    frascos_exatos = ml_necessarios / tamanho_frasco
    frascos_final = math.ceil(frascos_exatos)
    
    # 3. Sobra e Dias Extras
    ml_vendidos = frascos_final * tamanho_frasco
    sobra_ml = ml_vendidos - ml_necessarios
    
    # Lógica nova: Converte a sobra (ml) em gotas e divide pelo uso diário
    sobra_em_gotas = sobra_ml * dados_med['gotas_ml']
    dias_extras = int(sobra_em_gotas / gotas_por_dia)
    
    # --- RESULTADO ---
    st.divider()
    st.markdown("### ✅ Resultado")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("Frascos", f"{frascos_final} cx")
    col_res2.metric("Volume Necessário", f"{ml_necessarios:.1f} mL")
    col_res3.metric("Total Gotas", f"{total_gotas}")
    
    # Exibe a sobra com a conversão em dias
    if sobra_ml > 0:
        st.info(
            f"💡 **Sobra:** Aproximadamente **{sobra_ml:.1f} mL** no último frasco.\n\n"
            f"🗓️ Essa quantidade rende cerca de **+{dias_extras} dias** extras de tratamento."
        )

else:
    st.write("👆 Clique para calcular.")
