import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Calculadora Farma", page_icon="💊")

# --- BANCO DE DADOS (Baseado no seu PDF) ---
# Dicionário com os dados dos medicamentos
medicamentos = {
    1: {"nome": "Exodus / Lexapro",      "gotas_ml": 20, "frasco_ml": 15},
    2: {"nome": "Daforin",               "gotas_ml": 20, "frasco_ml": 20},
    3: {"nome": "Tramal",                "gotas_ml": 40, "frasco_ml": 10},
    4: {"nome": "Lexotan",               "gotas_ml": 25, "frasco_ml": 20},
    5: {"nome": "Rivotril",              "gotas_ml": 25, "frasco_ml": 20},
    6: {"nome": "Haldol",                "gotas_ml": 20, "frasco_ml": 30},
    7: {"nome": "Amplictil",             "gotas_ml": 40, "frasco_ml": 20},
    8: {"nome": "Gardenal",              "gotas_ml": 40, "frasco_ml": 20},
    9: {"nome": "Neozine",               "gotas_ml": 40, "frasco_ml": 20},
    10: {"nome": "Neuleptil (1% ou 4%)", "gotas_ml": 40, "frasco_ml": 20},
}

# --- INTERFACE VISUAL (FRONT-END) ---
st.title("💊 Calculadora de Dispensação")
st.markdown("Use esta ferramenta para calcular a quantidade de frascos para **medicamentos controlados**.")

# Criando uma lista apenas com os nomes para o usuário escolher
opcoes_nomes = {med['nome']: id_med for id_med, med in medicamentos.items()}
nome_selecionado = st.selectbox("Selecione o Medicamento:", list(opcoes_nomes.keys()))

# Recuperando os dados do medicamento escolhido
id_selecionado = opcoes_nomes[nome_selecionado]
med = medicamentos[id_selecionado]

# Mostrando os dados técnicos na tela para conferência
st.info(f"**Parâmetros do {nome_selecionado}:** {med['gotas_ml']} gotas/mL | Frasco de {med['frasco_ml']} mL")

st.divider() # Linha divisória

# --- COLUNAS PARA ENTRADA DE DADOS ---
col1, col2 = st.columns(2)

with col1:
    gotas_por_dia = st.number_input("Gotas por DIA:", min_value=1, value=10, step=1)

with col2:
    dias_tratamento = st.number_input("Duração (DIAS):", min_value=1, value=30, step=1)

# --- LÓGICA DE VALIDAÇÃO (REGRA DE NEGÓCIO) ---
# Verifica a regra dos 60 dias automaticamente
if dias_tratamento > 60:
    st.error(f"⚠️ ATENÇÃO: {dias_tratamento} dias excede o limite legal de 60 dias para controlados!")
    confirmacao = st.checkbox("Estou ciente e quero calcular mesmo assim (Regime Especial)")
else:
    confirmacao = True

# --- BOTÃO DE CALCULAR ---
if st.button("Calcular Quantidade", type="primary"):
    if confirmacao:
        # Cálculos Matemáticos
        total_gotas = gotas_por_dia * dias_tratamento
        total_ml_necessario = total_gotas / med['gotas_ml']
        frascos_exatos = total_ml_necessario / med['frasco_ml']
        frascos_final = math.ceil(frascos_exatos)
        
        # Cálculo de Sobra
        total_ml_frascos = frascos_final * med['frasco_ml']
        sobra_ml = total_ml_frascos - total_ml_necessario
        dias_extras = int((sobra_ml * med['gotas_ml']) / gotas_por_dia)

        # --- EXIBIÇÃO DOS RESULTADOS ---
        st.success("Cálculo realizado com sucesso!")
        
        # Usando Métricas (Visual bonito com números grandes)
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Frascos a Comprar", f"{frascos_final} un", delta="Caixas Fechadas")
        col_res2.metric("Volume Total", f"{total_ml_necessario:.1f} mL")
        col_res3.metric("Sobra Estimada", f"{sobra_ml:.1f} mL")
        
        # Detalhe extra
        if dias_extras > 0:
            st.caption(f"💡 Dica: A sobra no frasco é suficiente para mais **{dias_extras} dias** de tratamento.")
            
    else:
        st.warning("O cálculo foi bloqueado devido à regra de 60 dias.")
