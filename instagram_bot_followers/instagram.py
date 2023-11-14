from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import pandas as pd
import time
import os
import re
import logging

logger = logging.getLogger()

#USERNAME = "testeiropy10"
#USERNAME = "odapalm22"
#PASSWORD = "palm22"
#USERNAME = "orlapalm23"
#PASSWORD = "palm230@"
USERNAME = "rogeriobolado71"
PASSWORD = "agoravai"

cidades_portugual = {'porto': 'Porto', 'braga': 'Braga','póvoa de varzim':'Póvoa de Varzim','lisboa':'Lisboa','faro':'Faro','coimbra':'Coimbra','aveiriro':'Aveiro','funchal':'Funchal','sintra':'Sintra','guimarães':'Guimarães'}

client = Client()

def init_bot_client():
    client.login(USERNAME,PASSWORD)
    

def determinar_cidade(biografia):
    cidades_portugal = {
        'porto': 'Porto', 'braga': 'Braga', 'póvoa de varzim': 'Póvoa de Varzim', 'lisboa': 'Lisboa', 'faro': 'Faro',
        'coimbra': 'Coimbra', 'aveiriro': 'Aveiro', 'funchal': 'Funchal', 'sintra': 'Sintra', 'guimarães': 'Guimarães'
    }
    if isinstance(biografia, list):
        biografia = ' '.join(biografia)
    biografia = biografia.lower()

    padrao_cidades = '|'.join(cidades_portugal.keys())
    regex = re.compile(padrao_cidades)

    matches = regex.findall(biografia)
    for match in matches:
        if match:
            return cidades_portugal.get(match)
        
    
def determinar_nacionalidade(biografia):
    paises = {'brasil': 'Brasil', 'portugal': 'Portugal', 'itália': 'Itália', 'australia': 'Australia', 'belgium': 'Belgium', 'france': 'France', 'alemanha': 'Alemanha', 'espanha': 'Espanha',
              'reino_unido': 'Reino Unido', 'holanda': 'Holanda', 'suica': 'Suíça', 'suecia': 'Suécia', 'noruega': 'Noruega', 'dinamarca': 'Dinamarca', 'austria': 'Áustria', 'grecia': 'Grécia',
              'polonia': 'Polônia', 'hungria': 'Hungria', 'canada': 'Canada','estados_unidos': 'Estados Unidos'}

    bandeiras = {'🇧🇷': 'Brasil', '🇵🇹': 'Portugal', '🇮🇹': 'Itália', '🇦🇺': 'Australia', '🇧🇪': 'Belgium', '🇫🇷': 'France', '🇩🇪': 'Alemanha', '🇪🇸': 'Espanha', '🇬🇧': 'Reino Unido', '🇳🇱': 'Holanda', '🇨🇭': 'Suíça', '🇸🇪': 'Suécia', '🇳🇴': 'Noruega', '🇩🇰': 'Dinamarca', '🇦🇹': 'Áustria', '🇬🇷': 'Grécia', '🇵🇱': 'Polônia', '🇭🇺': 'Hungria', '🇦🇷': 'Argentina', '🇨🇱': 'Chile', '🇨🇴': 'Colômbia', '🇻🇪': 'Venezuela',
              '🇺🇾': 'Uruguai', '🇵🇾': 'Paraguai', '🇪🇨': 'Equador', '🇧🇴': 'Bolívia', '🇵🇪': 'Peru', '🇺🇸': 'Estados Unidos', '🇨🇦': 'Canadá'}

    cidades_portugual = {'lisboa': 'Portugal', 'porto': 'Portugal', 'coimbra': 'Portugal', 'braga': 'Portugal', 'faro': 'Portugal', 'aveiro': 'Portugal'}

    if isinstance(biografia, list):
        biografia = ' '.join(biografia)
    biografia = biografia.lower()

    padrao_paises = '|'.join(paises.keys())
    padrao_bandeiras = '|'.join(re.escape(flag) for flag in bandeiras.keys())
    padrao_final = f'({padrao_paises})|({padrao_bandeiras})'
    regex = re.compile(padrao_final)

    encontrou_nacionalidade = False
    encontrou_cidade = False

    matches = regex.findall(biografia)
    for match in matches:
        for grupo in match:
            if grupo:
                if grupo.lower() in cidades_portugual.keys():
                    encontrou_cidade = True
                if not encontrou_nacionalidade:
                    encontrou_nacionalidade = True
                    if encontrou_cidade:
                        return 'Portugal'
                    return paises.get(grupo.lower()) or bandeiras.get(grupo)

                
def determinar_genero(generoUser):
    if not generoUser or not isinstance(generoUser, str):
        return "Entrada inválida"

    generoUser = generoUser.lower().strip()
    nomes_masculinos = [
    'murray', 'joao', 'john', 'josh', 'arthur', 'ronald','joshua','brock','alex',
    'jackie','odin','ryan','david','james','shintaro','eduardo','claudio',
    'isaac','ben','lord','guilherme','xander', 'jacob','marco','alexander','eddie',
    'francisco', 'felipe', 'lucas', 'enzo', 'gabriel', 'miguel', 'rafael', 'mateus', 
    'heitor', 'gustavo', 'otávio', 'leonardo', 'cauã', 'vinícius', 'lucca', 'davi', 
    'bruno', 'emanuel', 'carlos', 'matheus', 'júlio', 'vicente', 'diego', 'luís', 
    'ícaro', 'bruno', 'leandro', 'rodrigo', 'tiago', 'saulo', 'nícolas', 'antonio', 
    'fernando', 'geraldo', 'hélio', 'ígor', 'jorge', 'kauê', 'lauro', 'marcelo', 
    'nelson', 'orlando', 'paulo', 'quirino', 'ricardo', 'samuel', 'tomás', 'ulisses', 
    'valentin', 'wilson', 'yuri', 'zélio', 'abel', 'bento', 'cícero', 'danilo', 
    'eliseu', 'fabrício', 'gregório', 'hugo', 'ícaro', 'ivo', 'joaquim', 'kaique', 
    'laerte', 'maicon', 'natan', 'ôscar', 'patrício', 'quirino', 'ramon', 'sandro', 
    'tadeu', 'ubaldo', 'valter', 'wescley', 'yago', 'zico', 'adalberto', 'bernardo', 
    'caio', 'dário', 'elton', 'fabiano', 'gilmar', 'haroldo', 'ítalo', 'jacó', 
    'kevin', 'leônidas', 'manoel', 'natanael', 'octávio', 'péricles', 'quincas', 
    'raimundo', 'saul', 'teodoro', 'ulysses', 'valdo', 'washington', 'yago', 'zaqueu', 
    'ademar', 'baltazar', 'casimiro', 'décio', 'elias', 'florêncio', 'gilberto', 
    'hermínio', 'ícaro', 'jadiel', 'kaleb', 'lázaro', 'manassés', 'nélio', 'osmar', 
    'pascácio', 'querubim', 'régis', 'silvio', 'tácito', 'ugo', 'valdo', 'wálter', 
    'xavier', 'yago', 'zacarias', 'adriel', 'bernardo', 'cássio', 'décio', 'elísio', 
    'fernando', 'gerson', 'hermínio', 'ícaro', 'jairo', 'kelvin', 'lucas', 'márcio', 
    'nélson', 'olavo', 'paulo', 'quirino', 'ricardo', 'salomão', 'telmo', 'uelinton', 
    'vítor','adriano', 'bernardo', 'césar', 'dênis', 'emanuel', 'flávio', 'gabriel', 'henrique', 
    'ítalo', 'jonas', 'kelvin', 'luan', 'marcel', 'nathan', 'olívio', 'paulo', 'querubim', 
    'rafael', 'samuel', 'teodoro', 'úrsulo', 'vagner', 'wellington', 'xavier', 'yago', 
    'zaqueu', 'aldo', 'benício', 'ciro', 'damião', 'ezequiel', 'felipe', 'guilherme', 
    'hélio', 'ícaro', 'júnior', 'kevin', 'lucas', 'márcio', 'nélson', 'orfeu',
    'quirino', 'rafael', 'samuel', 'tadeu', 'uriel', 'vinícius', 'wellington', 'xavier', 
    'ygor', 'zacarias', 'augusto', 'bartolomeu', 'cícero', 'daniel', 'eder', 'fernando', 
    'gabriel', 'henrique', 'ícaro', 'joaquim', 'kauê', 'luan', 'marcos', 'nícolas', 
    'pedro', 'quirino', 'raul', 'samuel', 'tobias', 'ulisses', 'vitor', 'wiliam','jõao',
    'rui','joão','rafa','jose','andré','andre','zé','flavio','simao','lopes','sérgio','sergio',
    'filipe','dinis','alvaro','marcio','justino','rocio','vlad','léo','leo','angelo','yassin',
    'dario','dylan','borges','duarte','nicolas','nicolás','jordan','emiliano','chico','anibal',
    'ramiro','leonor','diogo','michael','joel','fabio','estevan','carther','cristiano','ronaldo',
    'sílvio','flavio','adilson','hélder','helder','gilberto','gil','patrick','tommy','gonçalo',
    'jony','jay','josé','jose','patric','hiago','brizzo','brandão','brandao','marcio','stivie',
    'renato','brito','paolo','fábio','nunes','nikolas','jhonson','alex','vando','ramalho',''
    'jardel','dennis','ivan','alexandre','nelthon','amorim','victor','amaro','anthony','xavi',
    'sergey','pablo','telmo','isaiah','felicio','cristophe','toni','rui','simão','simao','sérgio',
    'cédric'
    ]
    nomes_femininos = ['maria', 'joaquina', 'naty', 'ashley', 'marta', 'rose', 'cameron', 'becca', 'riley', 'jocelyn', 'josie', 'irene', 'mary', 'samantha', 'sarah', 'jasmine', 'emilia', 'angie', 
                'charlotte', 'lola', 'jennyfer', 'stace', 'ana', 'beatriz', 'carla', 'daniela', 'érica', 'fernanda', 'gabriela', 'helena', 'inês', 'juliana', 'karen', 'lara', 'mônica', 
                'natália', 'olívia', 'patrícia', 'quésia', 'raquel', 'sônia', 'tânia', 'úrsula', 'vanessa', 'wanda', 'ximena', 'yara', 'zara', 'adriana', 'bianca', 'catarina', 'dora', 
                'eunice', 'flávia', 'graça', 'íris', 'júlia', 'lídia', 'márcia', 'nádia', 'odete', 'querida', 'raíssa', 'sílvia', 'tânia', 'úrsula', 'vitória', 'xana', 'yara', 'zilda', 
                'adelaide', 'benedita', 'cecília', 'dalila', 'eulália', 'francisca', 'glória', 'hermínia', 'ingrid', 'joana', 'kátia', 'lúcia', 'marisa', 'nádia', 'odete', 'priscila', 
                'quitéria', 'ramona', 'sílvia', 'telma', 'úrsula', 'vera', 'wanda', 'ximena', 'yara', 'zara', 'alda', 'belinda', 'célia', 'dulce', 'elisa', 'felícia', 'glória', 'hilda',
                'inês', 'júlia', 'karen', 'lídia', 'mariana', 'nádia', 'olga', 'patrícia', 'querida', 'raquel', 'sílvia', 'teresa', 'úrsula', 'violeta','catia','barbara','daniela',
                'raisa','matilde','clésia','carolina','sara','luna','jéssica','lara','victoria','jéssica','jessica','tatiana','luana','léticia','leticia','matilde','babi','andreia',
                'vera','rita','mariá','iasmin','alina','margarida','carlota','ines','eleonora','antonia','ántonia','rita','teresa','carina','cláudia','iris','joana','kátia',
                'rosinha','hermelinda','julia','agata','valentina','isabela','sandra','melissa','catia','luna','soraia','carolina','nicole','inês','elise','madalena','marisol','luana',
                'liliana','emilie','tatiana','tatiane','staisy','bruna','laila','patty','scarlett','miriam','paula','patricia','cynthia','daniela'
    ]

    primeiro_nome = generoUser.split(' ')[0]

    if primeiro_nome in nomes_masculinos:
        return "Masculino"
    elif primeiro_nome in nomes_femininos:
        return "Feminino"
    else:
        return "Gênero desconhecido"

# Lista de contas
contas = ["gate13.pt"]

dados_usuario = {'Conta': [], 'Seguidores': [],'Nome_Completo': [],'Cidade_Nome': [],'Biografia': [],'Nacionalidade': [],'Gênero': []}

def obter_seguidores(client, contas):
    dados = {'Conta': [], 'Seguidores': []}
    
    if os.path.exists('seguidores2.csv'):
        pd.read_csv('seguidores2.csv')
    else:
        df = pd.DataFrame(columns=['Conta', 'Seguidores'])
        df.to_csv('seguidores2.csv', index=False)

    for conta in contas:
        try:
            profile_id = client.user_id_from_username(conta)
            print(profile_id)
            followers = client.user_followers_v1(profile_id,2000)
            print(followers)
            count = 0
            df = pd.read_csv('seguidores2.csv')
            for user_id, user_info in followers.items():
                if user_info.username not in df['Seguidores'].values:
                    dados['Conta'].append(conta)
                    dados['Seguidores'].append(user_info.username)
                    df = pd.DataFrame(dados)
                    df.to_csv('seguidores2.csv',index=False)
                    count += 1
                    print(count)
                    if count % 500 == 0:
                        print(f"Total de seguidores obtidos para {conta}: {count}")
                        client.logout()
                        time.sleep(180)
                        client.login(USERNAME,PASSWORD)
                        

        except Exception as e:
            print(f'Erro ao obter seguidores de {conta}: {str(e)}')
            pass
        
    client.logout()
  
def obter_info_usuarios(client):
    
    df = pd.read_excel('info_usuarios_gate.xlsx')
    df_resultado = pd.DataFrame(columns=['Seguidores', 'Nome_Completo', 'Biografia', 'Nacionalidade','Cidade', 'Gênero'])
    dados_usuario = {
        'Seguidores': [],
        'Nome_Completo': [],
        'Biografia': [],
        'Nacionalidade': [],
        'Cidade': [],
        'Gênero': []
    }
    for username in df['Seguidores']:
        try:
            user_info = client.user_info_by_username(username).dict()
            print(user_info['username'])
            dados_usuario['Seguidores'].append(user_info['username'])
            dados_usuario['Nome_Completo'].append(user_info['full_name'])
            dados_usuario['Biografia'].append(user_info['biography'])
            nacionalidade = determinar_nacionalidade(user_info['biography'])
            dados_usuario['Nacionalidade'].append(nacionalidade)
            cidade = determinar_cidade(user_info['biography'])
            dados_usuario['Cidade'].append(cidade)
            genero = determinar_genero(user_info['full_name'])
            dados_usuario['Gênero'].append(genero)
            
            df_resultado = pd.DataFrame(dados_usuario)
            df_resultado.to_excel('info_usuarios_gate_v2.xlsx', index=False)
            
        except Exception as e:
            print(f'Erro ao obter informações do usuário {username}: {str(e)}')

    
init_bot_client()
#login_user()
#obter_seguidores(client, contas)
obter_info_usuarios(client)
