import time
import logging
import pandas as pd
import numpy as np
import re
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException,NoSuchFrameException,TimeoutException,NoSuchWindowException,StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---- USADO ---- #
#USERNAME = "fabricioalves1808"
#PASSWORD = "fabi12"
#---- NAO USADO----#
#USERNAME = "paulovergueiro1"
#PASSWORD = "pv090298"
#USERNAME = "soniavilela20231"
#PASSWORD = "sv20231@"

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
GET_FULL_FOLLOWERS = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span"
FOLLOWERS_BOX = "//a[contains(@href, '/followers')]"
SCROLL_FOLLOWERS_BOX = "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
DIV_ALL = "._aano"

names_set = set()
processed_links_count = 0
contador_condicao = 1
contador_loop = 0
tempo_de_espera = 1.8
scroll_init = 170
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
tempo_de_espera_init = 1.2
first_number_scroll = 720
line = "###############"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
           'Upgrade-Insecure-Requests': '1'}

def processar_lote_scroll(scroll_box, processed_links_count):
    links = scroll_box.find_elements(By.TAG_NAME, 'a')
    return list(map(lambda name: name.text, filter(lambda name: name.text != '', links[processed_links_count:])))


chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox") 
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
        wait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,SECOND_AGORA_NAO_BUTTON)))
        driver.find_element(By.XPATH,SECOND_AGORA_NAO_BUTTON).click()
    except TimeoutException:
        pass
    
    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,SEARCH_BOX)))
    driver.find_element(By.XPATH,SEARCH_BOX).click()
    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,SEND_ACCOUNT_BOX)))
    driver.find_element(By.XPATH,SEND_ACCOUNT_BOX).send_keys("industriaclub")
    time.sleep(2)
    driver.find_element(By.XPATH,CLICK_FIRST_ACCOUNT).click()
    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,GET_FULL_FOLLOWERS)))
    seguidores = driver.find_element(By.XPATH,GET_FULL_FOLLOWERS).text
    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,FOLLOWERS_BOX)))
    
    match = re.match(r"([\d.,]+)\s*([a-zA-Z]+)",seguidores)
    if match:
        numero = match.group(1)
        unidade = match.group(2)
        numero = float(numero.replace(',', ''))
        multiplicador = 1
        if unidade.lower() == "mil":
            multiplicador = 1000
        resultado = (numero * multiplicador) / 100
        resultado_inteiro = int(resultado)
    
    driver.find_element(By.XPATH,FOLLOWERS_BOX).click()
    print(f"{line} Follower Pass !!! {line}")
    time.sleep(3)
    driver.execute_script("document.body.style.zoom='75%'")
    time.sleep(2)
    scroll_box = driver.find_element(By.XPATH,SCROLL_FOLLOWERS_BOX)
    
    for _ in range(resultado_inteiro):
            for _ in range(scroll_init):
                while True:
                    try: 
                        driver.execute_script(f"arguments[0].scrollBy(0, {first_number_scroll});", scroll_box)
                        time.sleep(tempo_de_espera)
                        links = scroll_box.find_elements(By.TAG_NAME, 'a')
                        new_names = list(map(lambda name: name.text, filter(lambda name: name.text != '', links[processed_links_count:])))
            
                             
                        links_array = np.array(new_names)
                        processed_links_count = len(links_array)
                        if not os.path.isfile("seguidores_industriaclub_time_final_v2.csv") or os.stat("seguidores_industriaclub_time_final_v2.csv").st_size == 0:
                            df = pd.DataFrame(links_array, columns=['Seguidores'])
                            df.to_csv("seguidores_industriaclub_time_final_v2.csv", mode='a', index=False, encoding='utf-8')
                        else:
                            df = pd.DataFrame(links_array)
                            df.to_csv("seguidores_industriaclub_time_final_v2.csv", mode='a', header=False, index=False, encoding='utf-8')
                        
                        script = """
                        var elements = document.querySelectorAll('img');
                        for (var i = 0; i < elements.length; i++) {
                            elements[i].remove();
                        }
                        """
                        driver.execute_script(script)
                        script_button = """
                        var elements = document.querySelectorAll('button');
                        for (var i = 0; i < elements.length; i++) {
                            elements[i].remove();
                        }
                        """
                        driver.execute_script(script_button)
                        script_a = """
                        var elements = document.querySelectorAll('a');
                        for (var i = 0; i < elements.length; i++) {
                            elements[i].parentNode.removeChild(elements[i]);
                        }
                        """
                        driver.execute_script(script_a)
                        break
                    
                    except StaleElementReferenceException or NoSuchWindowException or NoSuchElementException:
                        print("A barra de carregamento travou")
                        break
            
            #try:
                #div_all = driver.find_element(By.CSS_SELECTOR,DIV_ALL)
                #div_children = div_all.find_elements(By.TAG_NAME,"div")
                #div_all = driver.find_elements(By.CSS_SELECTOR, 'div.x1dm5mii.x16mil14')                    
                #for i in reversed(range(15)):
                #        div = div_all[i]
                #        driver.execute_script("arguments[0].style.display='none'", div)
                        
                #div_all = driver.find_elements(By.CSS_SELECTOR, 'div.x1dm5mii.x16mil14')  
                            
            #except StaleElementReferenceException or NoSuchElementException or NoSuchWindowException:
               #print("Achou elemento mas apagou tudo pelo jeito")
                #break
            
            #for link in links:
            #    if link.tag_name == 'a':
            #        driver.execute_script("""
            #            var element = arguments[0];
            #            element.parentNode.removeChild(element);
            #        """, link)
            
            contador_loop += 1
            if contador_loop % 1 == 0:
                print("Entrou time sum")
                tempo_de_espera += tempo_de_espera_init
                time.sleep(300)
                #time.sleep(time_sleep_count)
                #time_sleep_count+= 60
                
            if contador_loop % 6 == 0:
                scroll_init = 120
                tempo_de_espera = 12
                first_number_scroll = 680
                print("Entrou no 30 min")
                time.sleep(300)
                
            if contador_loop % 9 == 0:
                scroll_init = 100
                print("Entrou no 30 min")
                time.sleep(600)
                