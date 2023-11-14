import pandas as pd

# Substitua 'seu_arquivo.csv' pelo caminho do seu arquivo CSV
caminho_arquivo = 'seguidores_gareporto_versao1.csv'

# Carregando o CSV em um DataFrame do pandas
df = pd.read_csv(caminho_arquivo)

# Removendo linhas com valores vazios na coluna 'Seguidores'
df = df.dropna(subset=['Seguidores'])

# Exibindo o DataFrame resultante
print(df)
