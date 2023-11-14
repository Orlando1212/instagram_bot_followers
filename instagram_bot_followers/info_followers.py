import time
import logging
import pandas as pd
import numpy as np
import re
import chardet
import pyautogui
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException,NoSuchFrameException,TimeoutException,NoSuchWindowException,StaleElementReferenceException,ElementClickInterceptedException,ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed


USERNAME = "fabricioalves1808"
PASSWORD = "fabi12"
#USERNAME = "soniavilela20231"
#PASSWORD = "sv20231@"
#SERNAME = "gersonalencar20232"
#PASSWORD = "palmeiras23"
#SERNAME = "paulovergueiro1"
#PASSWORD = "pv090298"
#USERNAME = "telmaborges2023"
#PASSWORD = "tb42001@"
#USERNAME = "soniavilela20231"
#PASSWORD = "sv20231@"
#USERNAME = "telmaborges2023"
#PASSWORD = "tb42001@"
#USERNAME = "gilbertosilva9889"
#PASSWORD = "flamengo20"
#USERNAME = "rodrigoguerra221"
#PASSWORD = "santos90"
#USERNAME = "monicanogueira2003"
#PASSWORD = "mn20031@"

SCROLL = "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]"
SCRIPT_SIZE = "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div"
USERNAME_BOX = "//*[@id='loginForm']/div/div[1]/div/label/input"
PASS_BOX = "//*[@id='loginForm']/div/div[2]/div/label/input"
SUBMIT_CLICK = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button"
AGORA_NAO_BUTTON = "//div[contains(text(),'Agora não')]"
SECOND_AGORA_NAO_BUTTON = "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"
SEARCH_BOX = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a"
SEND_ACCOUNT_BOX = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input"
CLICK_FIRST_ACCOUNT_V2 = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a"
CLICK_FIRST_ACCOUNT = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a[1]"
FULL_NAME_TEXT = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div[1]"
BIO_TEXT = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/h1"
USERNAME_TEXT = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/a"
OCORREU_UM_ERRO = ""

processed_links_count = 0
contador_condicao = 1
contador_loop = 0
tempo_de_espera = 1.2
scroll_init = 95
string_count_1020 = 5000
string_count_3000 = 3000
processed_usernames = set()
string_count_3500 = 3500
integer_count_2 = int(string_count_1020)
string_count_1000 = 4500
integer_count_1 = int(string_count_1000)
links_list = []
links_dict = {}
scroll_count = 5
tempo_de_espera_init = 0.45
first_number_scroll = 800
line = "###############"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
           'Upgrade-Insecure-Requests': '1'}

chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--headless")
for key, value in headers.items():
    chrome_options.add_argument(f'--header={key}:{value}')
    
#df = pd.read_excel('info_usuarios_gate_v3.xlsx')
#df_resultado = pd.DataFrame(columns=['Seguidores', 'Nome_Completo', 'Biografia', 'Nacionalidade','Cidade', 'Gênero'])
dados_usuario = {
    'Seguidores': [],
    'Nome_Completo': [],
    'Biografia': [],
    'Nacionalidade': [],
    'Cidade': [],
    'Gênero': []
    }

def determinar_cidade(biografia):
    cidades_portugal = {
        'porto': 'Porto', 'braga': 'Braga', 'póvoa de varzim': 'Póvoa de Varzim', 'lisboa': 'Lisboa', 'faro': 'Faro',
        'coimbra': 'Coimbra', 'aveiriro': 'Aveiro', 'funchal': 'Funchal', 'sintra': 'Sintra', 'guimarães': 'Guimarães',
        'cascais':'Cascais','viseu':'Viseu','viana do castelo':'Viana do castelo','setúbal':'Setubal','albufeira':'Albufeira',
        'lagos':'Lagos','leira':'Leira','tomar':'Tomar','vila nova da gaia':'Vila nova da gaia','portimão':'Portimão',
        'mondim de basto':'Mondim de Basto','lisbon':'Lisboa'
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
              'polonia': 'Polônia', 'hungria': 'Hungria', 'canada': 'Canada','estados_unidos': 'Estados Unidos','pt':'Portugal'}

    bandeiras = {'🇧🇷': 'Brasil', '🇵🇹': 'Portugal', '🇮🇹': 'Itália', '🇦🇺': 'Australia', '🇧🇪': 'Belgium', '🇫🇷': 'France', '🇩🇪': 'Alemanha', '🇪🇸': 'Espanha', '🇬🇧': 'Reino Unido', '🇳🇱': 'Holanda', '🇨🇭': 'Suíça', '🇸🇪': 'Suécia', '🇳🇴': 'Noruega', '🇩🇰': 'Dinamarca', '🇦🇹': 'Áustria', '🇬🇷': 'Grécia', '🇵🇱': 'Polônia', '🇭🇺': 'Hungria', '🇦🇷': 'Argentina', '🇨🇱': 'Chile', '🇨🇴': 'Colômbia', '🇻🇪': 'Venezuela',
              '🇺🇾': 'Uruguai', '🇵🇾': 'Paraguai', '🇪🇨': 'Equador', '🇧🇴': 'Bolívia', '🇵🇪': 'Peru', '🇺🇸': 'Estados Unidos', '🇨🇦': 'Canadá'}

    cidades_portugal = {
        'porto': 'Portugal', 'braga': 'Portugal', 'póvoa de varzim': 'Portugal', 'lisboa': 'Portugal', 'faro': 'Portugal',
        'coimbra': 'Portugal', 'aveiriro': 'Portugal', 'funchal': 'Portugal', 'sintra': 'Portugal', 'guimarães': 'Portugal',
        'cascais':'Portugal','viseu':'Portugal','viana do castelo':'Portugal','setúbal':'Portugal','albufeira':'Portugal',
        'lagos':'Portugal','leira':'Portugal','tomar':'Portugal','vila nova da gaia':'Portugal','portimão':'Portugal',
        'mondim de basto':'Portugal','lisbon':'Portugal'
    }

    if isinstance(biografia, list):
        biografia = ' '.join(biografia)
    biografia = biografia.lower()

    for cidade in cidades_portugal.keys():
        if cidade in biografia:
            return 'Portugal'

    padrao_paises = '|'.join(paises.keys())
    padrao_bandeiras = '|'.join(re.escape(flag) for flag in bandeiras.keys())
    padrao_final = f'({padrao_paises})|({padrao_bandeiras})'
    regex = re.compile(padrao_final)

    encontrou_nacionalidade = False

    matches = regex.findall(biografia)
    for match in matches:
        for grupo in match:
            if grupo:
                if not encontrou_nacionalidade:
                    encontrou_nacionalidade = True
                    return paises.get(grupo.lower()) or bandeiras.get(grupo)

                
def determinar_genero(generoUser):
    if not generoUser or not isinstance(generoUser, str):
        return "N/A"

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
    'cédric','nuno','juan','deni','pete','indre','igor','antónio','wagner','christian','gareth',
    'renan','mário','emmanuel','ruben','jonathas','justin','matteo','lázaro','lazaro','ross',
    'javier','raúl','toni','rúben','óscar','julian','kobe','joão',
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
                'liliana','emilie','tatiana','tatiane','staisy','bruna','laila','patty','scarlett','miriam','paula','patricia','cynthia','daniela','simone','thais','rute','aida','aída',
                'klaudia','clara','cassandra','angela','mónica','monica','sofia','joanina','kleidi','karolayn','juliane','gaia','haruka','bonnie','valeria','rayanne','ninna','mika',
                'renata','elena','jéssica','lila','manu','lucía','vanesa','bárbara','inês','marina'
    ]

    primeiro_nome = generoUser.split(' ')[0]

    if primeiro_nome in nomes_masculinos:
        return "Masculino"
    elif primeiro_nome in nomes_femininos:
        return "Feminino"
    else:
        return "N/A"

with webdriver.Chrome(options=chrome_options) as driver:
    driver.get("https://www.instagram.com/")
    wait(driver, 8).until(EC.element_to_be_clickable((By.XPATH,USERNAME_BOX)))
    driver.find_element(By.XPATH,USERNAME_BOX).send_keys(USERNAME)
    driver.find_element(By.XPATH,PASS_BOX).send_keys(PASSWORD)
    wait(driver, 8).until(EC.element_to_be_clickable((By.XPATH,SUBMIT_CLICK)))
    driver.find_element(By.XPATH,SUBMIT_CLICK).click()
    wait(driver, 8).until(EC.element_to_be_clickable((By.XPATH,AGORA_NAO_BUTTON)))
    driver.find_element(By.XPATH,AGORA_NAO_BUTTON).click()
    try:
        wait(driver, 8).until(EC.element_to_be_clickable((By.XPATH,SECOND_AGORA_NAO_BUTTON)))
        driver.find_element(By.XPATH,SECOND_AGORA_NAO_BUTTON).click()
    except TimeoutException:
        pass

    if os.path.isfile('info_usuarios_gareporto_versao_final.xlsx'):
        df_existente_xlsx = pd.read_excel("info_usuarios_gareporto_versao_final.xlsx")
        df_existente = pd.read_csv('seguidores_gareporto_versao1.csv')
        ultimo_seguidor_existente = df_existente_xlsx['Seguidores'].iloc[-1]

        if ultimo_seguidor_existente in df_existente['Seguidores'].values: 
            index_start = df_existente[df_existente['Seguidores'] == ultimo_seguidor_existente].index[0]
            df = df_existente.iloc[index_start:]
            
            for index, row in df_existente_xlsx.iterrows():
                dados_usuario['Seguidores'].append(row['Seguidores'])
                dados_usuario['Nome_Completo'].append(row['Nome_Completo'])
                dados_usuario['Biografia'].append(row['Biografia'])
                dados_usuario['Nacionalidade'].append(row['Nacionalidade'])
                dados_usuario['Cidade'].append(row['Cidade'])
                dados_usuario['Gênero'].append(row['Gênero'])
            
        for username in df['Seguidores']:
            print(username)
            try:
                wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,SEARCH_BOX)))
                driver.find_element(By.XPATH,SEARCH_BOX).click()
                try:
                    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,SEND_ACCOUNT_BOX)))
                    send_account_box = driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys(username)
                except ElementClickInterceptedException:
                    pass
                
                except TimeoutException:
                    pass
                
                except ElementNotInteractableException:
                    pass
                
                except StaleElementReferenceException:
                    pass
                
                try:
                    wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,CLICK_FIRST_ACCOUNT)))
                    driver.find_element(By.XPATH,CLICK_FIRST_ACCOUNT).click()
                
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except ElementClickInterceptedException:
                    pass
                
                try:
                    driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys(Keys.ESCAPE)
                                       
                except:
                    pass
                
                try:
                    wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,CLICK_FIRST_ACCOUNT_V2)))
                    driver.find_element(By.XPATH,CLICK_FIRST_ACCOUNT_V2).click()
                except TimeoutException:
                    pass
                
                except StaleElementReferenceException:
                    pass
                
                except ElementClickInterceptedException:
                    pass
                
                try:
                    driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys(Keys.ESCAPE)
                                       
                except:
                    pass
                try:
                    time.sleep(1.5)
                    wait(driver, 8).until(EC.presence_of_element_located((By.XPATH,USERNAME_TEXT)))
                    username_text = driver.find_element(By.XPATH,USERNAME_TEXT).text
                    #wait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME,'h2')))
                    #username_text = driver.find_element(By.TAG_NAME,'h2').text
                    print(username_text)
                
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except NoSuchElementException:
                    pass
                    
                try:
                    wait(driver, 2).until(EC.presence_of_element_located((By.XPATH,FULL_NAME_TEXT)))
                    full_name = driver.find_element(By.XPATH,FULL_NAME_TEXT).text
                    
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except NoSuchElementException:
                    #print("Algum erro de nao ter encontrado o elemento")
                    pass
                    
                try:
                    wait(driver, 2).until(EC.presence_of_element_located((By.XPATH,BIO_TEXT)))
                    bio_text = driver.find_element(By.XPATH,BIO_TEXT).text
                
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except NoSuchElementException:
                    #print("Algum erro de nao ter encontrado o elemento")
                    pass
                
                if not dados_usuario['Biografia']:
                    dados_usuario['Seguidores'].append(username_text)
                    dados_usuario['Nome_Completo'].append(full_name)
                    dados_usuario['Biografia'].append(bio_text)
                    nacionalidade = determinar_nacionalidade(bio_text)
                    dados_usuario['Nacionalidade'].append(nacionalidade)
                    cidade = determinar_cidade(bio_text)
                    dados_usuario['Cidade'].append(cidade)
                    genero = determinar_genero(full_name)
                    dados_usuario['Gênero'].append(genero)

                elif bio_text and bio_text != dados_usuario['Biografia'][-1]:
                        dados_usuario['Seguidores'].append(username_text)
                        dados_usuario['Nome_Completo'].append(full_name)
                        dados_usuario['Biografia'].append(bio_text)
                        nacionalidade = determinar_nacionalidade(bio_text)
                        dados_usuario['Nacionalidade'].append(nacionalidade)
                        cidade = determinar_cidade(bio_text)
                        dados_usuario['Cidade'].append(cidade)
                        genero = determinar_genero(full_name)
                        dados_usuario['Gênero'].append(genero)

                df_resultado = pd.DataFrame(dados_usuario)
                df_resultado.to_excel('info_usuarios_gareporto_versao_final.xlsx',encoding = 'utf-8', index=False)
                contador_loop+= 1

                
                if contador_loop % 500 == 0:
                    time.sleep(1800)
                
            
            except NoSuchElementException :
                print("Ocorreu um erro ao consultar as informaçoes dos seguidores")
                            
            except ElementClickInterceptedException:
                print("Não achou o search")
                driver.quit()
                pass
            
            except TimeoutException:
                print("Não achou o search")
                driver.quit()
                pass
            
            except ElementNotInteractableException:
                print("Não achou o search")
                driver.quit()
                pass
        
    else:
        df = pd.read_csv('seguidores_gareporto_versao1.csv',encoding ='utf-8')
        for username in df['Seguidores']:
            print(username)
            try:
                wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,SEARCH_BOX)))
                driver.find_element(By.XPATH,SEARCH_BOX).click()
                try:
                    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,SEND_ACCOUNT_BOX)))
                    send_account_box = driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys(username)
                except ElementClickInterceptedException:
                    pass
                
                except TimeoutException:
                    pass
                
                except ElementNotInteractableException:
                    pass
                
                except StaleElementReferenceException:
                    pass
                
                try:
                    wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,CLICK_FIRST_ACCOUNT)))
                    driver.find_element(By.XPATH,CLICK_FIRST_ACCOUNT).click()
                
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except ElementClickInterceptedException:
                    pass
                
                try:
                    driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys(Keys.ESCAPE)
                                       
                except:
                    pass
                
                try:
                    wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,CLICK_FIRST_ACCOUNT_V2)))
                    driver.find_element(By.XPATH,CLICK_FIRST_ACCOUNT_V2).click()
                except TimeoutException:
                    pass
                
                except StaleElementReferenceException:
                    pass
                
                except ElementClickInterceptedException:
                    pass
                
                try:
                    driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys(Keys.ESCAPE)
                                       
                except:
                    pass
                try:
                    time.sleep(1.5)
                    wait(driver, 8).until(EC.presence_of_element_located((By.XPATH,USERNAME_TEXT)))
                    username_text = driver.find_element(By.XPATH,USERNAME_TEXT).text
                    #wait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME,'h2')))
                    #username_text = driver.find_element(By.TAG_NAME,'h2').text
                    print(username_text)
                
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except NoSuchElementException:
                    pass
                    
                try:
                    wait(driver, 2).until(EC.presence_of_element_located((By.XPATH,FULL_NAME_TEXT)))
                    full_name = driver.find_element(By.XPATH,FULL_NAME_TEXT).text
                    
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except NoSuchElementException:
                    #print("Algum erro de nao ter encontrado o elemento")
                    pass
                    
                try:
                    wait(driver, 2).until(EC.presence_of_element_located((By.XPATH,BIO_TEXT)))
                    bio_text = driver.find_element(By.XPATH,BIO_TEXT).text
                
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except NoSuchElementException:
                    #print("Algum erro de nao ter encontrado o elemento")
                    pass
                
                if not dados_usuario['Biografia']:
                    dados_usuario['Seguidores'].append(username_text)
                    dados_usuario['Nome_Completo'].append(full_name)
                    dados_usuario['Biografia'].append(bio_text)
                    nacionalidade = determinar_nacionalidade(bio_text)
                    dados_usuario['Nacionalidade'].append(nacionalidade)
                    cidade = determinar_cidade(bio_text)
                    dados_usuario['Cidade'].append(cidade)
                    genero = determinar_genero(full_name)
                    dados_usuario['Gênero'].append(genero)

                elif bio_text and bio_text != dados_usuario['Biografia'][-1]:
                        dados_usuario['Seguidores'].append(username_text)
                        dados_usuario['Nome_Completo'].append(full_name)
                        dados_usuario['Biografia'].append(bio_text)
                        nacionalidade = determinar_nacionalidade(bio_text)
                        dados_usuario['Nacionalidade'].append(nacionalidade)
                        cidade = determinar_cidade(bio_text)
                        dados_usuario['Cidade'].append(cidade)
                        genero = determinar_genero(full_name)
                        dados_usuario['Gênero'].append(genero)

                df_resultado = pd.DataFrame(dados_usuario)
                df_resultado.to_excel('info_usuarios_gareporto_versao_final.xlsx',encoding = 'utf-8', index=False)
                contador_loop+= 1

                
                if contador_loop % 500 == 0:
                    time.sleep(1800)
                
            
            except NoSuchElementException :
                print("Ocorreu um erro ao consultar as informaçoes dos seguidores")
                            
            except ElementClickInterceptedException:
                print("Não achou o search")
                driver.quit()
                pass
            
            except TimeoutException:
                print("Não achou o search")
                driver.quit()
                pass
            
            except ElementNotInteractableException:
                print("Não achou o search")
                driver.quit()
                pass
            

        