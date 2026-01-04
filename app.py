import streamlit as st

# --- 1. CONFIGURAÇÃO DA PÁGINA (Isso define o nome na aba e o ícone) ---
st.set_page_config(
    page_title="CalcFarma",  # O nome que aparece na aba do navegador
    page_icon="💊",          # O ícone (Favicon). Pode ser um emoji ou arquivo .png
    layout="centered",       # Centraliza o conteúdo no celular
    initial_sidebar_state="collapsed" # Esconde o menu lateral para parecer mais app
)

# --- 2. CABEÇALHO ---
st.title("Calculadora Pediátrica 💊")
st.markdown("**Medicamento:** Dipirona (500mg/mL)\n\n**Regra:** 1 gota por kg")

# --- 3. ENTRADA DE DADOS ---
# step=0.1 permite digitar pesos quebrados (ex: 12.5 kg)
peso = st.number_input("Digite o peso da criança (kg):", min_value=0.0, step=0.1, format="%.1f")

# --- 4. CONTROLE DE ESTADO (MEMÓRIA) ---
# O Streamlit apaga variáveis a cada clique, então usamos session_state para lembrar do resultado
if 'resultado' not in st.session_state:
    st.session_state.resultado = None
if 'tipo_msg' not in st.session_state:
    st.session_state.tipo_msg = "info" # pode ser 'success', 'warning' ou 'error'

# --- 5. LÓGICA E BOTÕES ---
col1, col2 = st.columns(2) # Cria duas colunas para os botões ficarem lado a lado

with col1:
    # Botão Calcular (Primary deixa ele destacado/vermelho no tema padrão)
    if st.button("Calcular", type="primary", use_container_width=True):
        if peso > 0:
            gotas = int(peso) # Regra: 1 gota por kg
            
            # Regra de Segurança (Teto)
            if gotas > 40:
                gotas = 40
                st.session_state.resultado = f"Dose Teto: {gotas} gotas (Máximo atingido)"
                st.session_state.tipo_msg = "warning"
            else:
                st.session_state.resultado = f"Dose Recomendada: {gotas} gotas"
                st.session_state.tipo_msg = "success"
        else:
            st.session_state.resultado = "Por favor, digite um peso válido."
            st.session_state.tipo_msg = "error"

with col2:
    # Botão Limpar
    if st.button("Limpar", use_container_width=True):
        st.session_state.resultado = None # Limpa a memória
        st.rerun() # Recarrega a página para limpar o campo numérico (reset visual)

# --- 6. EXIBIÇÃO DO RESULTADO ---
st.divider() # Uma linha divisória bonita

if st.session_state.resultado:
    if st.session_state.tipo_msg == "success":
        st.success(st.session_state.resultado, icon="✅")
    elif st.session_state.tipo_msg == "warning":
        st.warning(st.session_state.resultado, icon="⚠️")
    else:
        st.error(st.session_state.resultado, icon="❌")
