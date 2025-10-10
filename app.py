import streamlit as st
from utils import aplicar_estilo_customizado, carregar_dados

from utils import adicionar_fundo_css_animado

st.set_page_config(
    page_title="FDS Harpie - Tela inicial",
    page_icon="🧪",
    layout="centered"
)

aplicar_estilo_customizado()
adicionar_fundo_css_animado()

df_ghs, _ = carregar_dados() 

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

url_readme = "https://github.com/meanmathics/fds-harpie/blob/main/README.md"

st.markdown(f"""
    <div class="floating-container">
        <a href="{url_readme}" target="_blank">?</a>
    </div>
""", unsafe_allow_html=True)