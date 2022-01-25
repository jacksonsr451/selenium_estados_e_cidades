# Script simples utilizando Python e selenium.

## O objetivo bem simples:
Primeiro era de ir em algumas URLs expecificas e filtrar is dados 
de estado junto com a sigla, claro que poderia terfacilitado montando um 
dicionario contendo estes primeiros dados.

Mas em primeiro momento, mantendo neste estilo e alterando para frente.

Em segundo momento o script entra em uma base de dados da wikipedia, percorre 
por todas as linhas em uma tabela, filtra e captura todos os dados, 
posteriormente buscando em links relacionados aos municípios de cada estado
e coleta cada um os colocando em uma lista.

Após a coleta de todos os dados, o script, em uma pasta especifica
states_files_json, monta para cada estado em um .json com suas cidades contidas em uma 
lista!
