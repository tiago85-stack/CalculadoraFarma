import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Farmácia",
    page_icon="💊",
    layout="centered"
)

# --- BANCO DE DADOS (Padrões sugeridos) ---
# Fonte: Tabela de conversão enviada
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

# --- TÍTULO ---
st.title("💊 Calculadora de Dispensação")
st.markdown("---")

# --- BARRA LATERAL (ENTRADAS) ---
st.sidebar.header("1. Configuração do Medicamento")

# Seleção do Nome
nome_med = st.sidebar.selectbox(
    "Medicamento:",
    options=medicamentos.keys()
)

# Pega os dados padrão do dicionário
dados_padrao = medicamentos[nome_med]

# MOSTRAR E EDITAR O TAMANHO DO FRASCO
# Aqui está a mudança: O valor vem do dicionário, mas o usuário pode alterar.
st.sidebar.markdown("---")
st.sidebar.subheader("Ajuste do Frasco")
tamanho_frasco = st.sidebar.number_input(
    "Volume do Frasco (mL):",
    min_value=1.0,
    value=float(dados_padrao['frasco_padrao']), # Carrega o padrão aqui
    step=1.0,
    help="Se o genérico tiver tamanho diferente, altere este valor."
)

st.sidebar.info(
    f"**{nome_med}**\n\n"
    f"Gotejamento fixo: {dados_padrao['gotas_ml']} gts/mL\n"
    f"Frasco considerado: {tamanho_frasco} mL"
)

st.sidebar.markdown("---")
st.sidebar.header("2. Posologia")

col1, col2 = st.sidebar.columns(2)
with col1:
    gotas_por_dia = st.number_input("Gotas/Dia", min_value=1, value=10)
with col2:
    dias_tratamento = st.number_input("Dias", min_value=1, value=30)

# --- VALIDAÇÃO 60 DIAS ---
if dias_tratamento > 60:
    st.warning(f"⚠️ **ATENÇÃO:** {dias_tratamento} dias excede o limite comum de 60 dias para controlados.")

# --- BOTÃO E CÁLCULOS ---
if st.sidebar.button("Calcular Quantidade", type="primary"):
    
    # 1. Quantas gotas o paciente vai tomar no total?
    total_gotas = gotas_por_dia * dias_tratamento
    
    # 2. Quantos mL isso representa? (Baseado na densidade do remédio)
    total_ml_necessario = total_gotas / dados_padrao['gotas_ml']
    
    # 3. Quantos frascos precisa? (Usando o tamanho_frasco que você editou)
    frascos_exatos = total_ml_necessario / tamanho_frasco
    frascos_finais = math.ceil(frascos_exatos)
    
    # 4. Cálculo de Sobra
    volume_comprado = frascos_finais * tamanho_frasco
    sobra_ml = volume_comprado - total_ml_necessario
    
    # Estimar quantos dias a sobra rende
    dias_extras = 0
    if gotas_por_dia > 0:
        dias_extras = int((sobra_ml * dados_padrao['gotas_ml']) / gotas_por_dia)

    # --- RESULTADO NA TELA ---
    st.subheader("Resultado")
    
    # Containers visuais
    c1, c2, c3 = st.columns(3)
    c1.metric("Frascos a Comprar", f"{frascos_finais} cx")
    c2.metric("Volume Real Necessário", f"{total_ml_necessario:.1f} mL")
    c3.metric("Total de Gotas", f"{total_gotas}")

    st.success(f"O paciente levará **{volume_comprado} mL** no total.")

    # Análise de Sobra
    if sobra_ml > 0:
        with st.expander("ℹ️ Detalhes da Sobra (Clique para ver)"):
            st.write(f"Vai sobrar aproximadamente **{sobra_ml:.1f} mL** no último frasco.")
            st.write(f"Essa sobra daria para cobrir mais **{dias_extras} dias** de tratamento.")
            
else:
    st.info("👈 Ajuste os dados na barra lateral e clique em Calcular.")
