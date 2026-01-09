import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora de Dispensação",
    page_icon="💊",
    layout="centered"
)

# --- BANCO DE DADOS (Baseado no seu PDF) ---
# Dica de Eng. Software: Usar o Nome como 'Chave' facilita a busca no Selectbox
medicamentos = {
    "Exodus / Lexapro":      {"gotas_ml": 20, "frasco_ml": 15},
    "Daforin":               {"gotas_ml": 20, "frasco_ml": 20},
    "Tramal":                {"gotas_ml": 40, "frasco_ml": 10},
    "Lexotan":               {"gotas_ml": 25, "frasco_ml": 20},
    "Rivotril":              {"gotas_ml": 25, "frasco_ml": 20},
    "Haldol":                {"gotas_ml": 20, "frasco_ml": 30},
    "Amplictil":             {"gotas_ml": 40, "frasco_ml": 20},
    "Gardenal":              {"gotas_ml": 40, "frasco_ml": 20},
    "Neozine":               {"gotas_ml": 40, "frasco_ml": 20},
    "Neuleptil (1% ou 4%)":  {"gotas_ml": 40, "frasco_ml": 20},
}

# --- TÍTULO E CABEÇALHO ---
st.title("💊 Calculadora de Dispensação")
st.markdown("Calcula a quantidade de frascos baseada na **tabela de controlados**.")
st.markdown("---")

# --- BARRA LATERAL (SIDEBAR) PARA ENTRADAS ---
st.sidebar.header("Prescrição Médica")

# 1. Seleção do Medicamento
nome_med = st.sidebar.selectbox(
    "Selecione o Medicamento:",
    options=medicamentos.keys()
)

# Recupera os dados do medicamento selecionado
dados_med = medicamentos[nome_med]

# Mostra detalhes do medicamento escolhido na tela principal
st.info(f"**Medicamento Selecionado:** {nome_med} \n\n "
        f"💧 Gotejamento: {dados_med['gotas_ml']} gts/mL | 📦 Frasco: {dados_med['frasco_ml']} mL")

# 2. Entradas de valores (usando colunas para ficar lado a lado)
col1, col2 = st.sidebar.columns(2)

with col1:
    gotas_por_dia = st.number_input("Gotas/Dia", min_value=1, value=10, step=1)

with col2:
    dias_tratamento = st.number_input("Duração (Dias)", min_value=1, value=30, step=1)

# --- VALIDAÇÃO DA REGRA DE 60 DIAS ---
if dias_tratamento > 60:
    st.warning(f"⚠️ **ATENÇÃO:** O tratamento de {dias_tratamento} dias excede o limite sugerido de 60 dias para controlados.")

# --- LÓGICA DE CÁLCULO ---
# Botão para calcular (opcional no Streamlit, mas bom para UX)
if st.sidebar.button("Calcular Quantidade"):
    
    # Cálculos Matemáticos
    total_gotas = gotas_por_dia * dias_tratamento
    total_ml_necessario = total_gotas / dados_med['gotas_ml']
    frascos_exatos = total_ml_necessario / dados_med['frasco_ml']
    frascos_finais = math.ceil(frascos_exatos)
    
    # Cálculo de Sobra
    ml_totais_comprados = frascos_finais * dados_med['frasco_ml']
    sobra_ml = ml_totais_comprados - total_ml_necessario
    dias_extras = int((sobra_ml * dados_med['gotas_ml']) / gotas_por_dia)

    # --- EXIBIÇÃO DOS RESULTADOS ---
    st.divider()
    st.subheader("Resultado da Análise")

    # Usando métricas visuais (Big Numbers)
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric(label="Frascos a Comprar", value=f"{frascos_finais} un.")
    
    with col_res2:
        st.metric(label="Volume Necessário", value=f"{total_ml_necessario:.1f} mL")
        
    with col_res3:
        st.metric(label="Total de Gotas", value=f"{total_gotas}")

    # Exibição da sobra em formato de mensagem
    if sobra_ml > 0:
        st.success(f"💡 **Gestão de Sobra:** Vai sobrar aprox. **{sobra_ml:.1f} mL** no último frasco. \n\n"
                   f"Isso cobre cerca de **+{dias_extras} dias** além do previsto.")

else:
    st.write("👈 Configure a receita na barra lateral e clique em **Calcular**.")
