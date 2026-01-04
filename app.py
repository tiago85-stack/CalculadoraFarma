import streamlit as st

# Configuração da página (Título e ícone da aba)
st.set_page_config(page_title="CalcFarma", page_icon="💊")

st.title("Calculadora Pediátrica 💊")
st.write("Dose base: Dipirona (500mg/mL) - 1 gota/kg")

# Entrada de dados
peso = st.number_input("Digite o peso da criança (kg):", min_value=0.0, step=0.1, format="%.1f")

# Criando colunas para os botões ficarem lado a lado (igual você queria)
col1, col2 = st.columns(2)

# Variável para controlar o estado (se calculou ou não)
if 'resultado' not in st.session_state:
    st.session_state.resultado = ""

with col1:
    if st.button("Calcular", type="primary", use_container_width=True):
        if peso > 0:
            gotas = int(peso)
            msg_extra = ""
            if gotas > 40:
                gotas = 40
                msg_extra = " (Teto máximo atingido!)"
                st.warning("⚠️ Atenção: Dose limitada a 40 gotas.")
            
            st.session_state.resultado = f"Dose: {gotas} gotas{msg_extra}"
        else:
            st.error("Digite um peso válido.")

with col2:
    if st.button("Limpar", use_container_width=True):
        st.session_state.resultado = ""
        # O Streamlit recarrega a página ao clicar, limpando visualmente

# Mostra o resultado (se existir)
if st.session_state.resultado:
    st.success(st.session_state.resultado)