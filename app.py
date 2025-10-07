# --- INÍCIO DO CÓDIGO PARA O ARQUIVO app.py ---

import streamlit as st
import pandas as pd

# --- CARREGAMENTO E PREPARAÇÃO DOS DADOS ---
# Esta parte garante que a aplicação encontre os arquivos CSV.
try:
    df_ghs = pd.read_csv('GHS.csv')
    df_frases_p = pd.read_csv('Frases P.csv')
except FileNotFoundError:
    st.error("Erro: Verifique se os arquivos 'GHS.csv' e 'Frases p.csv' estão na mesma pasta que o app.py")
    st.stop() # Interrompe a execução se os arquivos não forem encontrados

# Corrigindo os nomes das colunas e criando a chave de busca
# (Ajuste os nomes das colunas aqui se forem diferentes)
nome_coluna_classificacao = 'Classe de Perigo'
nome_coluna_categoria = 'Categoria'
df_ghs['chave_classificacao_completa'] = df_ghs[nome_coluna_classificacao].str.strip() + ' ' + df_ghs[nome_coluna_categoria].astype(str).str.strip()


# --- LÓGICA PRINCIPAL (A FUNÇÃO QUE VOCÊ CRIOU) ---
def processar_classificacoes(lista_de_classificacoes: list):
    if not lista_de_classificacoes:
        return None

    dados_filtrados = df_ghs[df_ghs['chave_classificacao_completa'].isin(lista_de_classificacoes)]
    if dados_filtrados.empty:
        return None

    palavra_advertencia = "N/A"
    if 'Perigo' in dados_filtrados['Palavra de Advertência'].unique():
        palavra_advertencia = 'Perigo'
    elif 'Atenção' in dados_filtrados['Palavra de Advertência'].unique():
        palavra_advertencia = 'Atenção'

    pictogramas = dados_filtrados['Pictogramas'].dropna().unique().tolist()
    frases_h = (dados_filtrados['Código da Frase H'] + " " + dados_filtrados['Texto da Frase H']).dropna().unique().tolist()

    codigos_p_coletados = []
    # (Ajuste os nomes das colunas P se forem diferentes)
    for coluna in ['Frases P (Prevenção)', 'Frases P (Resposta)', 'Frases P (Armazenamento)', 'Frases P (Disposição)']:
        if coluna in dados_filtrados.columns:
            codigos_p_coletados.extend(dados_filtrados[coluna].dropna().tolist())

    codigos_p_unicos = list(set(codigos_p_coletados))
    
    # (Ajuste os nomes das colunas 'Código da Frase P' e 'Texto da Frase P' se forem diferentes)
    frases_p_finais = df_frases_p[df_frases_p['Codigo_Prec'].isin(codigos_p_unicos)]['Texto_Prec'].tolist()

    resultado = {
        'palavra_advertencia': palavra_advertencia,
        'pictogramas': pictogramas,
        'frases_h': frases_h,
        'frases_p': frases_p_finais
    }
    return resultado

# --- CONSTRUÇÃO DA INTERFACE WEB COM STREAMLIT ---

st.set_page_config(layout="wide") # Deixa a página mais larga
st.title("Assistente de Geração de FDS - Seção 2")
st.markdown("Uma ferramenta para automatizar a criação da seção de identificação de perigos.")

# Pega a lista completa de classificações do dataframe para usar na caixa de seleção
lista_de_classificacoes = df_ghs['chave_classificacao_completa'].unique()

st.sidebar.header("Parâmetros de Entrada")
selecionadas = st.sidebar.multiselect(
    'Selecione as classificações de perigo do produto:',
    lista_de_classificacoes
)

if st.sidebar.button('Gerar Seção 2'):
    if selecionadas:
        info_fds = processar_classificacoes(selecionadas)
        
        st.header("Resultado Gerado")
        
        col1, col2 = st.columns([1, 4]) # Cria duas colunas para organizar a exibição
        
        with col1:
            st.subheader("Pictogramas")
            if info_fds and info_fds['pictogramas']:
                # Tenta exibir as imagens da pasta 'pictogramas'
                for pic in info_fds['pictogramas']:
                    try:
                        # Assumimos que as imagens são .png, ajuste se necessário
                        st.image(f'pictogramas/{pic}.png', width=100) 
                    except Exception as e:
                        st.warning(f"Imagem {pic}.png não encontrada na pasta 'pictogramas'.")
            else:
                st.write("Nenhum pictograma aplicável.")

        with col2:
            st.subheader("Palavra de Advertência")
            st.info(info_fds['palavra_advertencia'])

            st.subheader("Frases de Perigo (H)")
            for frase in info_fds['frases_h']:
                st.write(frase)

            st.subheader("Frases de Precaução (P)")
            for frase in info_fds['frases_p']:
                st.write(f"- {frase}")
                
    else:
        st.sidebar.warning("Por favor, selecione ao menos uma classificação de perigo.")

# --- FIM DO CÓDIGO ---