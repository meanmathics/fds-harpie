import streamlit as st
import pandas as pd

def aplicar_estilo_customizado():
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stHeader"] {
                display: none;
            }
            .main .block-container {
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
            }
            div[data-testid="stVerticalBlock"] > div:first-child {
                margin-top: 0rem !important;
            }
            .stApp {
                background-color: #FFFFFF;
                color: marine;
            .back-button-container {
                position: fixed;
                top: 15px;
                left: 15px;
                z-index: 100;
            }
            h1, h2, h3 {
                color: marine;
                text-align: center;
                padding-bottom: 10px;
            }
            .texto-pequeno {
                font-size: 18px;
                line-height: 1.5;
            }
            .stMultiSelect > div[data-baseweb="select"] > div {
                background-color: #FFFFFF;
                border: 1px solid #1c83e1;
            }
            .stButton>button {
                border: 1px solid red;
                border-radius: 5px;
                color: red;
                background-color: transparent;
                padding: 2px 5px;
                transition: box-shadow 0.3s ease-in-out, color 0.3s ease-in-out;
            }
            .stButton>button:hover {
                color: #FF4B4B;
                background-color: white;
                box-shadow: 0 0 15px #ffffff;
            }
        </style>
    """, unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    df_ghs = pd.read_csv('data/GHS.csv')
    df_frases_p = pd.read_csv('data/Frases p.csv')
    
    df_ghs['chave_classificacao_completa'] = df_ghs['Classe de Perigo'].str.strip() + ' ' + df_ghs['Categoria'].astype(str).str.strip()
    return df_ghs, df_frases_p

def processar_classificacoes(lista_de_classificacoes, df_ghs, df_frases_p):
    if not lista_de_classificacoes:
        return None

    dados_filtrados = df_ghs[df_ghs['chave_classificacao_completa'].isin(lista_de_classificacoes)]
    if dados_filtrados.empty:
        st.warning("Nenhuma classificação correspondente foi encontrada.")
        return None

    valores_advertencia = dados_filtrados['Palavra de Advertência'].dropna().unique()
    
    valores_normalizados = [str(valor).lower().strip() for valor in valores_advertencia]

    palavra_advertencia = "Não aplicável"
    if 'perigo' in valores_normalizados:
        palavra_advertencia = 'PERIGO'
    elif 'atenção' in valores_normalizados:
        palavra_advertencia = 'Atenção'

    pictogramas = dados_filtrados['Pictogramas'].dropna().unique().tolist()
    frases_h = (dados_filtrados['Texto da Frase H']).dropna().unique().tolist()
    
    frases_p_agrupadas = {
        "Prevenção": [], "Resposta a Emergências": [],
        "Armazenamento": [], "Disposição": []
    }
    mapa_colunas_p = {
        'Frases P (Prevenção)': "Prevenção", 'Frases P (Resposta)': "Resposta a Emergências",
        'Frases P (Armazenamento)': "Armazenamento", 'Frases P (Disposição)': "Disposição Final"
    }

    for coluna_original, grupo in mapa_colunas_p.items():
        if coluna_original in dados_filtrados.columns:
            codigos_brutos = dados_filtrados[coluna_original].dropna().tolist()
            codigos_individuais = []
            for entrada in codigos_brutos:
                codigos_separados = str(entrada).split(',')
                for codigo in codigos_separados:
                    codigos_individuais.append(codigo.strip())
            
            codigos_unicos_para_lookup = list(set(codigos_individuais))

            if codigos_unicos_para_lookup:
                frases_do_grupo = df_frases_p[df_frases_p['Codigo_Prec'].isin(codigos_unicos_para_lookup)]['Texto_Prec'].tolist()
                frases_p_agrupadas[grupo] = frases_do_grupo
    
    resultado = {
        'palavra_advertencia': palavra_advertencia, 'pictogramas': pictogramas,
        'frases_h': frases_h, 'frases_p_agrupadas': frases_p_agrupadas
    }
    return resultado