# --- INÍCIO DO CÓDIGO ATUALIZADO ---

import streamlit as st
import pandas as pd

# --- CARREGAMENTO E PREPARAÇÃO DOS DADOS ---
try:
    df_ghs = pd.read_csv('GHS.csv')
    df_frases_p = pd.read_csv('Frases P.csv')
except FileNotFoundError:
    st.error("Erro: Verifique se os arquivos 'GHS.csv' e 'Frases p.csv' estão na mesma pasta que o app.py")
    st.stop()

# Ajuste os nomes das colunas aqui se forem diferentes no seu arquivo
nome_coluna_classificacao = 'Classe de Perigo'
nome_coluna_categoria = 'Categoria'
nome_coluna_codigo_p = 'Codigo_Prec'
nome_coluna_texto_p = 'Texto_Prec'
df_ghs['chave_classificacao_completa'] = df_ghs[nome_coluna_classificacao].str.strip() + ' ' + df_ghs[nome_coluna_categoria].astype(str).str.strip()


# --- SUBSTITUA A FUNÇÃO DE DEPURAÇÃO PELA VERSÃO CORRIGIDA ---
def processar_classificacoes(lista_de_classificacoes: list):
    # O modo de depuração não é mais necessário, então podemos remover os st.write
    if not lista_de_classificacoes:
        return None

    dados_filtrados = df_ghs[df_ghs['chave_classificacao_completa'].isin(lista_de_classificacoes)]
    if dados_filtrados.empty:
        # Adicionamos um aviso caso a filtragem não encontre nada
        st.warning("Nenhuma classificação correspondente foi encontrada. Verifique se o texto selecionado está correto.")
        return None

    palavra_advertencia = "N/A"
    if 'Perigo' in dados_filtrados['Palavra de Advertência'].unique():
        palavra_advertencia = 'Perigo'
    elif 'Atenção' in dados_filtrados['Palavra de Advertência'].unique():
        palavra_advertencia = 'Atenção'

    pictogramas = dados_filtrados['Pictogramas'].dropna().unique().tolist()
    frases_h = (dados_filtrados['Código da Frase H'] + " " + dados_filtrados['Texto da Frase H']).dropna().unique().tolist()

    # --- INÍCIO DA CORREÇÃO NA LÓGICA DAS FRASES P --- # <-- MUDANÇA CRÍTICA AQUI
    
    frases_p_agrupadas = {
        "Prevenção": [], "Resposta a Emergências": [],
        "Armazenamento": [], "Disposição": []
    }
    mapa_colunas_p = {
        'Frases P (Prevenção)': "Prevenção", 'Frases P (Resposta)': "Resposta a Emergências",
        'Frases P (Armazenamento)': "Armazenamento", 'Frases P (Disposição)': "Disposição"
    }

    for coluna_original, grupo in mapa_colunas_p.items():
        if coluna_original in dados_filtrados.columns:
            
            # Pega todos os valores da coluna, que podem conter múltiplos códigos
            codigos_brutos = dados_filtrados[coluna_original].dropna().tolist()
            
            codigos_individuais = []
            for entrada in codigos_brutos:
                # Quebra a string por vírgula para separar os códigos
                codigos_separados = str(entrada).split(',')
                for codigo in codigos_separados:
                    # Adiciona cada código limpo (sem espaços extras) à nossa lista
                    codigos_individuais.append(codigo.strip())
            
            # Remove duplicatas da nossa lista de códigos individuais
            codigos_unicos_para_lookup = list(set(codigos_individuais))

            if codigos_unicos_para_lookup:
                # Procura todos os códigos individuais na tabela de frases P
                frases_do_grupo = df_frases_p[df_frases_p[nome_coluna_codigo_p].isin(codigos_unicos_para_lookup)][nome_coluna_texto_p].tolist()
                frases_p_agrupadas[grupo] = frases_do_grupo
                
    # --- FIM DA CORREÇÃO ---

    resultado = {
        'palavra_advertencia': palavra_advertencia,
        'pictogramas': pictogramas,
        'frases_h': frases_h,
        'frases_p_agrupadas': frases_p_agrupadas
    }
    return resultado

# --- CONSTRUÇÃO DA INTERFACE WEB COM STREAMLIT ---

st.set_page_config(layout="wide")
st.title("FDS-Harpie")
st.markdown("Uma ferramenta simples para garantir a conformidade da seção 2 e da rotulagem de produtos químicos conforme a ABNT 14725:2023")

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
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.subheader("Pictogramas")
            if info_fds and info_fds['pictogramas']:
                for pic in info_fds['pictogramas']:
                    try:
                        st.image(f'pictogramas/{pic}.png', width=100) 
                    except Exception as e:
                        st.warning(f"Imagem {pic}.png não encontrada.")
            else:
                st.write("Nenhum pictograma aplicável.")

        with col2:
            st.subheader("Palavra de Advertência")
            st.info(info_fds['palavra_advertencia'])

            st.subheader("Frases de Perigo (H)")
            for frase in info_fds['frases_h']:
                st.write(frase)

            # --- INÍCIO DA MUDANÇA NA EXIBIÇÃO --- # <-- MUDANÇA AQUI
            st.subheader("Frases de Precaução (P)")
            frases_agrupadas = info_fds.get('frases_p_agrupadas', {})
            
            # Itera sobre o dicionário de grupos e frases
            for grupo, frases in frases_agrupadas.items():
                if frases: # Só mostra o grupo se ele tiver frases
                    st.markdown(f"**{grupo}:**")
                    for frase in frases:
                        st.write(f"- {frase}")
            # --- FIM DA MUDANÇA NA EXIBIÇÃO ---
                
    else:
        st.sidebar.warning("Por favor, selecione ao menos uma classificação de perigo.")

# --- FIM DO CÓDIGO ATUALIZADO ---