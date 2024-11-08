import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# configuração do driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.kabum.com.br/hardware/memoria-ram'
driver.get(url)

# função para extrair os dados de cada placa (por página)
def extrair_ram(driver):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sc-27518a44-4.kVoakD.productLink')))
    rams = driver.find_elements(By.CSS_SELECTOR, 'a.sc-27518a44-4.kVoakD.productLink')
    for ram in rams:
        try:
            imgRam = ram.find_element(By.CSS_SELECTOR, 'img.imageCard')
            imgRam = imgRam.get_attribute('src')
            print(imgRam)
            
            nomeRam = ram.find_element(By.CSS_SELECTOR, 'span.sc-d79c9c3f-0.nlmfp.sc-27518a44-9.iJKRqI.nameCard')
            print(nomeRam.text)

            precoRam = ram.find_element(By.CSS_SELECTOR, 'span.sc-57f0fd6e-2.hjJfoh.priceCard')
            print(precoRam.text)

        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
            continue

# extrai as placas da primeira página
extrair_ram(driver)

# try para navegar nas próximas páginas e extrair as informações das placas
while True:
    try:
        # validação se o botão "Próxima Página" é clicável
        botao_proxima_pagina = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nextLink'))
        )
        print("Botão 'Próxima Página' encontrado.")     
        
        # usando JS para clicar diretamente no botão
        driver.execute_script("arguments[0].click();", botao_proxima_pagina)
        print("Botão 'Próxima Página' clicado.")
        
        # aguarda o carregamento da nova página
        WebDriverWait(driver, 15).until(EC.staleness_of(botao_proxima_pagina))
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sc-27518a44-4.kVoakD.productLink'))
        )
        print("Nova página carregada.")
        
        # extrai novamente as placas após as validações
        extrair_ram(driver)
    except Exception as e:
        if "element could not be scrolled into view" in str(e):
            print("O botão 'Próxima Página' não pôde ser encontrado.")
        else:
            print("Não há mais páginas para navegar ou ocorreu um erro:", e)
        break