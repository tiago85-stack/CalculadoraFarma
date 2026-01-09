import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Farmácia Central",
    page_icon="💊",
    layout="centered" # Isso já garante que o conteúdo fique no meio
)

# --- ESTILIZAÇÃO CSS (Opcional, para deixar os inputs mais bonitos) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS ---
medicamentos = {
    "Exodus / Lexapro":      {"gotas_ml": 20, "frasco_padrao": 15},
    "Daforin":               {"gotas_ml": 20, "frasco_padrao": 20},
    "Tramal":                {"gotas_ml": 40, "frasco_padrao": 10},
    "Lexotan":               {"gotas_ml": 25, "frasco_padrao": 20},
    "Rivotril":              {"gotas_ml": 25, "frasco_padrao": 20},
    "Haldol":                {"gotas_ml": 20, "frasco_padrao": 30},
    "Amplictil":             {"gotas_ml": 40, "frasco_padrao": 20},
    "Gardenal":              {"gotas_ml": 40, "frasco_padrao": 20},
    "Neozine":               {"gotas_ml": 40, "frasco_padrao": 20},
    "Neuleptil (1% ou 4%)":  {"gotas_ml": 40, "frasco_padrao": 20},
}

# --- CABEÇALHO ---
st.title("💊 Calculadora de Dispensação")
st.caption("Ferramenta para cálculo de frascos de medicamentos controlados.")
st.markdown("---")

# --- BLOCO 1: SELEÇÃO DO MEDICAMENTO ---
st.subheader("1. Escolha o Medicamento")

# Cria duas colunas para dividir a seleção da informação técnica
c1, c2 = st.columns([2, 1]) 

with c1:
    nome_med = st.selectbox("Selecione na lista:", options=medicamentos.keys())
    dados_med = medicamentos[nome_med]

with c2:
    # Mostra os dados técnicos num card estático ao lado da seleção
    st.info(f"**Padrão Tabela:**\n\n💧 {dados_med['gotas_ml']} gts/mL\n\n📦 {dados_med['frasco_padrao']} mL")

st.markdown("---")

# --- BLOCO 2: CONFIGURAÇÃO DO FRASCO (Opção A/B) ---
st.subheader("2. Configuração do Frasco")

# Aqui usamos um container para agrupar essa lógica visualmente
with st.container():
    col_radio, col_input = st.columns(2)
    
    with col_radio:
        tipo_frasco = st.radio(
            "Qual apresentação será vendida?",
            ("Opção A: Padrão da Tabela", "Opção B: Genérico/Outro")
        )

    with col_input:
        if tipo_frasco == "Opção A: Padrão da Tabela":
            tamanho_frasco = float(dados_med['frasco_padrao'])
            st.success(f"🔒 Volume fixado em **{tamanho_frasco} mL**")
        else:
            tamanho_frasco = st.number_input(
                "Digite o volume do Genérico (mL):",
                min_value=1.0,
                value=float(dados_med['frasco_padrao']),
                step=1.0
            )

st.markdown("---")

# --- BLOCO 3: POSOLOGIA ---
st.subheader("3. Posologia da Receita")

col_dias, col_gotas = st.columns(2)

with col_gotas:
    gotas_por_dia = st.number_input("Quantas Gotas por Dia?", min_value=1, value=10)

with col_dias:
    dias_tratamento = st.number_input("Duração do Tratamento (Dias)", min_value=1, value=30)

# Validação visual imediata
if dias_tratamento > 60:
    st.error(f"⚠️ Atenção: {dias_tratamento} dias ultrapassa o limite sugerido de 60 dias.")

# --- BOTÃO DE AÇÃO (Largo) ---
if st.button("CALCULAR QUANTIDADE", type="primary"):
    
    # --- CÁLCULOS ---
    total_gotas = gotas_por_dia * dias_tratamento
    ml_necessarios = total_gotas / dados_med['gotas_ml']
    
    frascos_exatos = ml_necessarios / tamanho_frasco
    frascos_final = math.ceil(frascos_exatos)
    
    ml_total_comprado = frascos_final * tamanho_frasco
    sobra_ml = ml_total_comprado - ml_necessarios
    
    # --- RESULTADO CENTRALIZADO ---
    st.markdown("### ✅ Resultado")
    
    # Usando container para destacar o resultado
    with st.container():
        r1, r2, r3 = st.columns(3)
        r1.metric("Frascos a Comprar", f"{frascos_final} cx", delta="Recomendado")
        r2.metric("Volume Necessário", f"{ml_necessarios:.1f} mL")
        r3.metric("Volume Vendido", f"{ml_total_comprado:.1f} mL")
    
    if sobra_ml > 0:
        st.info(f"💡 **Nota ao Paciente:** Sobrará aprox. **{sobra_ml:.1f} mL** no último frasco.")

else:
    st.write("👆 Preencha os dados acima e clique em calcular.")
