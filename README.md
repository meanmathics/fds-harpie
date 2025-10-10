FDS Harpie Assistente Inteligente para Rotulagem GHS

Autor Rafael M.
Versão 1.0 (Alpha)
Link: https://fds-harpie.streamlit.app/

1. Introdução

O FDS Harpie é uma ferramenta web desenvolvida para simplificar e automatizar a criação dos elementos de rotulagem da Seção 2 de uma Ficha de Dados de Segurança (FDS), de acordo com as normas do GHS (Sistema Globalmente Harmonizado de Classificação e Rotulagem de Produtos Químicos).

O objetivo deste documento é explicar, de forma clara para um técnico ou profissional de química, a lógica por trás do sistema, sem a necessidade de conhecimento em programação.

2. O Problema A Complexidade da Rotulagem Manual

A elaboração manual da Seção 2 de uma FDS envolve um processo repetitivo e propenso a erros

Consulta a Múltiplas Fontes: É necessário consultar tabelas (como os anexos da ABNT NBR 14725) para cada classificação de perigo de um produto.

Consolidação de Informações: Um único produto pode ter múltiplas classificações de perigo. O técnico precisa consolidar pictogramas, frases de perigo (Frases H) e frases de precaução (Frases P), além de determinar a palavra de advertência correta seguindo uma regra de hierarquia.

Risco de Erro Humano: Esquecer uma frase, escolher o pictograma errado ou selecionar a palavra de advertência incorreta são riscos reais que podem ter consequências sérias.

3. A Solução Automatização e Padronização

O FDS Harpie atua como um assistente que automatiza todo o processo de consulta e consolidação, garantindo agilidade e precisão. A ferramenta utiliza as tabelas GHS como sua base de dados e aplica a lógica de consolidação de forma instantânea.

4. Como o Sistema Funciona Um Exemplo Prático

Vamos simular a rotulagem de um produto hipotético que possui duas classificações de perigo Líquidos oxidantes - Categoria 1 e Lesões oculares graves - Categoria 2A.

Passo 1 A Fonte de Dados (As Tabelas GHS)

O sistema tem como base as tabelas de classificação. Para cada perigo, a norma define um conjunto de elementos obrigatórios.

Para Líquidos oxidantes - Categoria 1, a tabela nos informa que os elementos são o pictograma GHS03 (chama sobre o círculo), a palavra de advertência Perigo, a Frase H H271 e um conjunto de Frases P.

![Tabela para Líquidos Oxidantes](https://raw.githubusercontent.com/meanmathics/fds-harpie/refs/heads/main/img/img1.png)

Para Lesões oculares graves - Categoria 2A, a tabela define o pictograma GHS07 (ponto de exclamação), a palavra de advertência Atenção, a Frase H H319 e outro conjunto de Frases P.

![Tabela para Danos Oculares](https://raw.githubusercontent.com/meanmathics/fds-harpie/refs/heads/main/img/img2.png)


A base de dados das Frases de Precaução também é carregada no sistema, contendo o texto completo para cada código P.

![Tabela de Frases de Precaução](https://raw.githubusercontent.com/meanmathics/fds-harpie/refs/heads/main/img/img3.png)


Passo 2 Seleção na Interface

O trabalho do técnico é simplesmente selecionar as classificações de perigo identificadas para o produto na tela inicial da aplicação.

![Tela Inicial](https://raw.githubusercontent.com/meanmathics/fds-harpie/refs/heads/main/img/img4.png)


Passo 3 A Lógica de Consolidação (O Cérebro do Sistema)

Após a seleção, o FDS Harpie aplica as seguintes regras automaticamente

Palavra de Advertência: O sistema verifica todas as palavras de advertência. Seguindo a regra de hierarquia, se Perigo estiver presente, ela será a palavra final, sobrepondo-se a Atenção. No nosso exemplo, o resultado é PERIGO.

Pictogramas: O sistema junta os pictogramas de todas as classificações e remove duplicatas. No nosso exemplo, ele une GHS03 e GHS07.

Frases de Perigo (H): O sistema junta as frases H de todas as classificações. No nosso exemplo, ele une H271 e H319.

Frases de Precaução (P): Esta é a etapa mais complexa. O sistema coleta todos os códigos P recomendados para ambas as classificações, remove os códigos duplicados e, em seguida, busca o texto completo de cada frase, organizando-os por categoria (Prevenção, Resposta a Emergências, Armazenamento, Disposição).

Passo 4 O Resultado Final

A aplicação exibe na tela de resultados todos os elementos já consolidados, formatados e prontos para serem inseridos na FDS ou no rótulo do produto.

![Tela de Resultado](https://raw.githubusercontent.com/meanmathics/fds-harpie/refs/heads/main/img/img5.png)


Portanto, ao utilizar este sistema, estes são os potenciais benefícios:

Redução de erros: Elimina o risco de falhas na consulta e consolidação manual das informações.
Eficiência: Reduz o tempo de elaboração significativamente.
Acurácia: Garante que a rotulagem esteja sempre consistente e de acordo com a base de dados atualizada.


