import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# configuração do driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.terabyteshop.com.br/hardware/placas-de-video'
driver.get(url)

# função para extrair os dados de cada placa (por página)
def extrair_placas(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.commerce_columns_item_inner')))
    placas = driver.find_elements(By.CSS_SELECTOR, 'div.commerce_columns_item_inner')
    for placa in placas:
        try:
            marca = placa.find_element(By.CSS_SELECTOR, 'h2')
            print(marca.text)
        except Exception as e:
            print(f"Erro ao extrair marca: {e}")
            continue

# extrai as placas da primeira página
extrair_placas(driver)

# try para navegar nas próximas páginas e extrair as placas de vídeo
while True:
    try:
        # Verifique se o botão "Próxima Página" está presente
        botao_proxima_pagina = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.arrow-down btn btn-pdmore'))
        )
        print("Botão 'Próxima Página' encontrado.")
        
        # movendo até o botão para garantir que esteja visível
        actions = ActionChains(driver)
        actions.move_to_element(botao_proxima_pagina).perform()
        
        # clicando no botão "Próxima Página"
        botao_proxima_pagina.click()
        print("Botão 'Próxima Página' clicado.")
        
        # aguardar o carregamento da nova página
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.commerce_columns_item_inner'))
        )
        print("Nova página carregada.")
        
        # extrai novamente as placas de vídeo
        extrair_placas(driver)

    except Exception as e:
        if "element could not be scrolled into view" in str(e):
            print("O botão 'Próxima Página' não pôde ser encontrado. Finalizando a navegação.")
        else:
            print("Não há mais páginas para navegar ou ocorreu um erro:", e)
        break

driver.quit()