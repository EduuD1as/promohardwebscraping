import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

# Configuração do driver do Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

url = 'https://www.kabum.com.br/hardware/placa-de-video-vga'
driver.get(url)
driver.maximize_window()

# Função para extrair os dados de cada placa (por página)
def extrair_placas(driver):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-27518a44-5')))
    placas = driver.find_elements(By.CSS_SELECTOR, 'div.sc-27518a44-5')
    for placa in placas:
        try:
            # Extraindo o nome da placa
            nomePlaca = placa.find_element(By.CSS_SELECTOR, 'span.sc-d79c9c3f-0')
            print(f"Nome: {nomePlaca.text}")
            
            # Extraindo o preço da placa
            precoPlaca = placa.find_element(By.CSS_SELECTOR, 'span.sc-3b515ca1-2')
            print(f"Preço: {precoPlaca.text}")
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
            continue

# Extrai as placas da primeira página
extrair_placas(driver)

# Tente navegar para as próximas páginas e extrair as placas de vídeo
while True:
    try:
        # Verifique se o botão "Próxima Página" está presente (clicável)
        botao_proxima_pagina = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nextLink'))
        )
        print("Botão 'Próxima Página' encontrado.")
        
        # Usando JavaScript para clicar diretamente no botão
        driver.execute_script("arguments[0].click();", botao_proxima_pagina)
        print("Botão 'Próxima Página' clicado.")
        
        # Aguardar o carregamento da nova página
        WebDriverWait(driver, 15).until(EC.staleness_of(botao_proxima_pagina))
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-27518a44-5'))
        )
        print("Nova página carregada.")
        
        # Extrai novamente as placas de vídeo
        extrair_placas(driver)
    except Exception as e:
        if "element could not be scrolled into view" in str(e):
            print("O botão 'Próxima Página' não pôde ser encontrado.")
        else:
            print("Não há mais páginas para navegar ou ocorreu um erro:", e)
        break

driver.quit()
