import instaloader
import pandas as pd

L = instaloader.Instaloader()
EX = instaloader.exceptions.InstaloaderException
FILENAME = "session.pickle"

# Autentique-se com a sua conta
L.login("oliveirasilva120312", "!Palmeiras11")  # Insira suas credenciais

# Lista de contas
contas = ["neopopfestival"]

dados = {'Conta': [], 'Seguidores': [], 'Nome_Completo': []}


    # Iterando sobre cada conta
for conta in contas:
        try:
            perfil = instaloader.Profile.from_username(L.context, conta)
            for seguidor in perfil.get_followers():
                print(seguidor)
                dados['Conta'].append(conta)
                dados['Seguidores'].append(seguidor.username)
                dados['Nome_Completo'].append(seguidor.full_name)

        except Exception as e:
            print(f'Erro ao obter seguidores de {conta}: {str(e)}')

df = pd.DataFrame(dados)
df.to_excel('seguidores.xlsx', index=False)

