import time
import logging
import pandas as pd
import numpy as np
import re
import os
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException,NoSuchFrameException,TimeoutException,NoSuchWindowException,StaleElementReferenceException,ElementClickInterceptedException,ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---- USADO ---- #
#USERNAME = "felipesantos22332023"
#PASSWORD = "fefesants2233"
#USERNAME = "soniavilela20231"
#PASSWORD = "sv20231@"
#USERNAME = "gersonalencar20232"
#PASSWORD = "palmeiras23"
#USERNAME = "mariatereza19621"
#PASSWORD = "palm2023"
#USERNAME = "forasteirodoido66"
#PASSWORD = "!Palmeiras11"
#USERNAME = "fabricioalves1808"
#PASSWORD = "fabi12"
#---- NAO USADO----#"
#USERNAME = "lucasmaciel1959"
#PASSWORD = "lm19591@"
#USERNAME = "gilbertosilva9889"
#PASSWORD = "flamengo20"
#USERNAME = "rodrigoguerra221"
#PASSWORD = "santos90"
#USERNAME = "telmaborges2023"
USERNAME = "leonelcamargo1923"
PASSWORD = "lc19231@"
#PASSWORD = "tb42001@"
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
CLICK_FIRST_ACCOUNT = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a[1]"
CLICK_FIRST_ACCOUNT_V2 = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a"
GET_FULL_FOLLOWERS = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span"
FOLLOWERS_BOX = "//a[contains(@href, '/following')]"
SEARCH_BOX_FOLLOWERS = "//input[@placeholder='Pesquisar']"
CLOSE_BOX_FOLLOWERS = "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button"
FIND_FOLLOWING = "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[2]/div/div/div/div/div/a/div/div/span"
DIV_ALL = "._aano"

flag_csv = True
processed_links_count = 0
contador_encontrados = 0
contador_condicao = 1
contador_loop = 0
tempo_de_espera = 1.7
scroll_init = 175
time_sleep_count = 180
string_count_1020 = 5500
string_count_3000 = 3000
string_count_3500 = 3500
integer_count_2 = int(string_count_1020)
string_count_1000 = 5000
integer_count_1 = int(string_count_1000)
links_list = []
links_dict = {}
scroll_count = 5
tempo_de_espera_init = 0.55
first_number_scroll = 770
line = "###############"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
           'Upgrade-Insecure-Requests': '1'}

lista_contas = ["gate13","gareporto","soundwavesfest","neopopfestival", "industriaclub"]


dados_usuario = {
    'Seguidores': [],
    }


chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")
for key, value in headers.items():
    chrome_options.add_argument(f'--header={key}:{value}')

with webdriver.Chrome(options=chrome_options) as driver:
    driver.get("https://www.instagram.com/")
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,USERNAME_BOX)))
    driver.find_element(By.XPATH,USERNAME_BOX).send_keys(USERNAME)
    driver.find_element(By.XPATH,PASS_BOX).send_keys(PASSWORD)
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,SUBMIT_CLICK)))
    driver.find_element(By.XPATH,SUBMIT_CLICK).click()
    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,AGORA_NAO_BUTTON)))
    driver.find_element(By.XPATH,AGORA_NAO_BUTTON).click()
    try:
        wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,SECOND_AGORA_NAO_BUTTON)))
        driver.find_element(By.XPATH,SECOND_AGORA_NAO_BUTTON).click()
    except TimeoutException:
        pass
    if flag_csv == False:    
        wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,SEND_ACCOUNT_BOX)))
        driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys("industriaclub")
        time.sleep(2)
        driver.find_element(By.XPATH,CLICK_FIRST_ACCOUNT).click()
        wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,GET_FULL_FOLLOWERS)))
        seguidores = driver.find_element(By.XPATH,GET_FULL_FOLLOWERS).text
        wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,FOLLOWERS_BOX)))
        
        driver.find_element(By.XPATH,FOLLOWERS_BOX).click()
        wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,SEARCH_BOX)))
        driver.find_element(By.XPATH,SEARCH_BOX).send_keys("orlandoliveira")
        if driver.find_elements(By.XPATH, "//*[text()='orlandoliveira']"):
            # Salve no arquivo CSV se o elemento for encontrado
            with open('output.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['orlandoliveira'])
        elif driver.find_elements(By.XPATH, "//span[contains(text(),'Nenhum resultado foi encontrado')]"):
            print("Nenhum resultado foi encontrado. Nenhum dado foi salvo no arquivo CSV.")
        else:
            print("Elemento não encontrado. Nenhum dado foi salvo no arquivo CSV.")
            
    
    else:
        
        if os.path.isfile('info_usuarios_gareporto.xlsx'):
            df_existente_xlsx = pd.read_excel("info_usuarios_gareporto.xlsx")
            df_existente = pd.read_excel("seguidores_encontrados.xlsx")
            ultimo_seguidor_existente = df_existente['Seguidores'].iloc[-1]
            print(ultimo_seguidor_existente)

        if ultimo_seguidor_existente in df_existente_xlsx['Seguidores'].values:
            index_start = df_existente_xlsx[df_existente_xlsx['Seguidores'] == ultimo_seguidor_existente].index[0]
            print(index_start)
            df = df_existente.iloc[index_start:]
            
            print(df['Seguidores'])
            
        for index, row in df_existente.iterrows():
                dados_usuario['Seguidores'].append(row['Seguidores'])
                
        for conta in df['Seguidores']:
                try:
                    wait(driver, 16).until(EC.element_to_be_clickable((By.XPATH,SEARCH_BOX)))
                    driver.find_element(By.XPATH,SEARCH_BOX).click()
                    try:
                            wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,SEND_ACCOUNT_BOX)))
                            send_account_box = driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys(conta)
                    except ElementClickInterceptedException:
                        pass
                    
                    except TimeoutException:
                        pass
                    
                    except ElementNotInteractableException:
                        pass
                    
                    except StaleElementReferenceException:
                        pass
                    
                except TimeoutException:
                    print("Erro de timeout")
                    continue
                
                try:
                    wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,CLICK_FIRST_ACCOUNT)))
                    driver.find_element(By.XPATH,CLICK_FIRST_ACCOUNT).click()
                
                except StaleElementReferenceException:
                    pass
                
                except TimeoutException:
                    pass
                
                except ElementClickInterceptedException:
                    pass
                
                time.sleep(0.5)
                try:
                    send_account_box = driver.find_element(By.XPATH,SEND_ACCOUNT_BOX)
                    send_account_box.send_keys(Keys.CONTROL + "a")
                    send_account_box.send_keys(Keys.DELETE)
                    
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
                    wait(driver, 6).until(EC.element_to_be_clickable((By.XPATH,FOLLOWERS_BOX)))
                    driver.find_element(By.XPATH,FOLLOWERS_BOX).click()
                
                except TimeoutException:
                    continue
                
                except NoSuchElementException:
                    continue
                
                time.sleep(2)
                try:
                    for i, conta_lista in enumerate(lista_contas):
                        try:
                            wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,SEARCH_BOX_FOLLOWERS)))
                            elemento = driver.find_element(By.XPATH,SEARCH_BOX_FOLLOWERS)
                            texto_a_digitar = conta_lista
                            for caractere in texto_a_digitar:
                                elemento.send_keys(caractere)
                                time.sleep(0.3)
                        except ElementClickInterceptedException:
                            print("Não encontrou o caminho do pesquisar")
                            
                        except TimeoutException:
                            print("Extorou o tempo")
                        
                        try:
                            wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,f"//span[contains(text(),'{conta_lista}')]")))
                            span_element = driver.find_element(By.XPATH,f"//span[contains(text(),'{conta_lista}')]")
                            print("Entrou")
                            contador_encontrados += 1
                            if contador_encontrados >= 2:
                                    dados_usuario['Seguidores'].append(conta)
                                    df_seguidores = pd.DataFrame(dados_usuario)
                                    df_seguidores.to_excel('seguidores_encontrados.xlsx', index=False)
                                    print("Dados dos seguidores salvos no arquivo XLSX.")
                                    contador_encontrados = 0
                                
                        except NoSuchElementException:
                            print("Nao encontrou o elemento")
                            pass
                        
                        except TimeoutException:
                            print("nao encontrou o elemento")
                            pass
                                
                        if driver.find_elements(By.XPATH, "//span[contains(text(),'Nenhum resultado foi encontrado')]"):
                            print(f"Nenhum resultado foi encontrado para a conta {conta_lista}.")
                            
                        else:
                            print(f"Elemento não encontrado para a conta {conta_lista}.")
                        
                        try:
                            send_account_box = driver.find_element(By.XPATH,SEARCH_BOX_FOLLOWERS)
                            send_account_box.send_keys(Keys.CONTROL + "a")
                            send_account_box.send_keys(Keys.DELETE)
                        except Exception:
                            print("nao apagou")
                            pass
                    
                    driver.find_element(By.XPATH,SEARCH_BOX_FOLLOWERS).send_keys(Keys.ESCAPE)
                    time.sleep(3)
                    
                except Exception as e:
                    pass
    
    