import streamlit as st
from utils import aplicar_estilo_customizado, carregar_dados


aplicar_estilo_customizado()
df_ghs, _ = carregar_dados() 

st.set_page_config(
    page_title="FDS Harpie - Tela inicial",
    page_icon="🧪",
    layout="centered"
)

st.title("FDS Harpie")
st.header("Passo 1: Selecione as Classificações de Perigo")

lista_de_classificacoes = df_ghs['chave_classificacao_completa'].unique()

selecionadas = st.multiselect(
    'Selecione todas as classificações aplicáveis ao produto:',
    lista_de_classificacoes
)


st.write("")
st.write("")

col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    if st.button("GERAR OS ELEMENTOS ✨", use_container_width=True):
        if selecionadas:
            st.session_state.classificacoes_selecionadas = selecionadas
            st.switch_page("pages/1_🏷️_Resultado.py")
        else:
            st.warning("Por favor, selecione ao menos uma classificação antes de continuar.")

if not selecionadas:
    if 'classificacoes_selecionadas' in st.session_state:
        del st.session_state.classificacoes_selecionadas