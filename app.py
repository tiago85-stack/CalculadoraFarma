import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Farmácia",
    page_icon="💊",
    layout="centered"
)

# --- ESTILO (Botão largo e campos limpos) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; margin-top: 10px; font-weight: bold; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS ATUALIZADO (Com Princípio Ativo) ---
# A chave agora inclui o Nome Comercial + Princípio Ativo para aparecer no menu
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

# Seleção única com nomes completos
nome_escolhido = st.selectbox(
    "Selecione o medicamento (Nome / Princípio Ativo):",
    options=medicamentos.keys()
)
dados_med = medicamentos[nome_escolhido]

# Mostra o padrão apenas como informação visual
st.info(f"ℹ️ **Padrão de Bula:** {dados_med['gotas_ml']} gotas/mL | Frasco de {dados_med['frasco_padrao']} mL")

st.markdown("---")

# --- 2. CONFIGURAÇÃO DO FRASCO (Opção B) ---
st.subheader("2. Qual frasco será entregue?")

# Layout de colunas para o rádio e o input ficarem organizados
col_tipo, col_vol = st.columns([1.5, 1])

with col_tipo:
    # Opção B textual como você pediu
    tipo_frasco = st.radio(
        "Selecione a apresentação:",
        ("Opção A: Padrão da Tabela", "Opção B: Genérico/Outro")
    )

with col_vol:
    # Lógica de edição
    if tipo_frasco == "Opção A: Padrão da Tabela":
        # Se for padrão, fixa o valor mas mostra desabilitado (ou apenas informativo)
        tamanho_frasco = st.number_input(
            "Volume (mL):",
            value=float(dados_med['frasco_padrao']),
            disabled=True # Trava a edição para evitar erro na Opção A
        )
    else:
        # Se for Opção B, libera a edição e foca no campo
        tamanho_frasco = st.number_input(
            "Volume do Genérico (mL):",
            min_value=1.0,
            value=float(dados_med['frasco_padrao']), # Começa com o padrão, mas editável
            step=1.0,
            help="Edite este valor conforme o frasco que você tem em mãos."
        )

st.markdown("---")

# --- 3. POSOLOGIA ---
st.subheader("3. Receita Médica")

c_gotas, c_dias = st.columns(2)
with c_gotas:
    gotas_por_dia = st.number_input("Gotas por Dia:", min_value=1, value=10)
with c_dias:
    dias_tratamento = st.number_input("Dias de Tratamento:", min_value=1, value=30)

if dias_tratamento > 60:
    st.error(f"⚠️ **Atenção:** {dias_tratamento} dias ultrapassa o limite de 60 dias.")

# --- CÁLCULO ---
if st.button("CALCULAR QUANTIDADE", type="primary"):
    
    # Matemática
    total_gotas = gotas_por_dia * dias_tratamento
    ml_necessarios = total_gotas / dados_med['gotas_ml']
    
    frascos_exatos = ml_necessarios / tamanho_frasco
    frascos_final = math.ceil(frascos_exatos)
    
    ml_total_comprado = frascos_final * tamanho_frasco
    sobra_ml = ml_total_comprado - ml_necessarios
    
    # --- RESULTADO ---
    st.markdown("### ✅ Resultado da Análise")
    
    with st.container():
        # Métricas lado a lado
        m1, m2, m3 = st.columns(3)
        m1.metric("Frascos a Entregar", f"{frascos_final} un")
        m2.metric("Volume do Tratamento", f"{ml_necessarios:.1f} mL")
        m3.metric("Volume Vendido", f"{ml_total_comprado:.1f} mL")
    
    if sobra_ml > 0:
        st.success(f"💡 **Informação:** Sobrará aprox. **{sobra_ml:.1f} mL** no último frasco.")

else:
    st.write("👆 Preencha e clique para calcular.")
