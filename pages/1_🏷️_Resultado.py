import streamlit as st
from utils import aplicar_estilo_customizado, carregar_dados, processar_classificacoes

aplicar_estilo_customizado()
df_ghs, df_frases_p = carregar_dados()

st.set_page_config(
    page_title="FDS Harpie - Resultado",
    page_icon="🏷️",
    layout="wide"
)

if st.button("⬅️ Voltar para a Seleção"):
    st.switch_page("app.py")

if 'classificacoes_selecionadas' in st.session_state and st.session_state.classificacoes_selecionadas:
    selecionadas = st.session_state.classificacoes_selecionadas
    info_fds = processar_classificacoes(selecionadas, df_ghs, df_frases_p)
    
    if info_fds:
        st.subheader("Frases de Perigo")
        frases_h_html = "<br>".join(info_fds['frases_h'])
        st.markdown(f'<div class="texto-pequeno">{frases_h_html}</div>', unsafe_allow_html=True)
        st.write("")

        st.subheader("Pictogramas")
        if info_fds['pictogramas']:
            num_pictogramas = len(info_fds['pictogramas'])
            cols = st.columns(num_pictogramas)
            for i, pic in enumerate(info_fds['pictogramas']):
                with cols[i]:
                    st.image(f'pictogramas/{pic}.png', width=80)
        st.write("")

        st.subheader("Palavra de Advertência")
        palavra = info_fds['palavra_advertencia']
        if palavra == 'PERIGO':
            st.markdown(f'<p class="texto-pequeno" style="color:red; font-weight:bold;">{palavra}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="texto-pequeno">{palavra}</p>', unsafe_allow_html=True)
        st.write("")

        st.subheader("Frases de Precaução")
        html_frases_p = ""
        frases_agrupadas = info_fds.get('frases_p_agrupadas', {})
        for grupo, frases in frases_agrupadas.items():
            if frases:
                html_frases_p += f"<b>{grupo}:</b><br>"
                for frase in frases:
                    html_frases_p += f"- {frase}<br>"
                html_frases_p += "<br>"
        st.markdown(f'<div class="texto-pequeno">{html_frases_p}</div>', unsafe_allow_html=True)
else:
    st.warning("Nenhuma classificação foi selecionada.")
    st.info("⬅️ Por favor, volte para a página principal para selecionar as classificações de perigo.")