import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure o driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Defina a URL e acesse a página
url = 'https://www.pichau.com.br/hardware/placa-de-video'
driver.get(url)

# Aguarda até que o elemento esteja presente (aumentando o tempo para 8 segundos)
try:
    WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiCardContent-root')))
    
    # Encontre todos os elementos que correspondem à classe desejada
    placas = driver.find_elements(By.CSS_SELECTOR, 'div.MuiCardContent-root')
    
    print(placas)

    # Verifique se há elementos antes de tentar acessar
    if placas:
        placa = placas[0]
        marca = placa.find_element(By.CSS_SELECTOR, 'h2.MuiTypography-root')
        print(marca.text)
    else:
        print("Nenhuma placa de vídeo encontrada.")

finally:
    # Encerre o driver
    driver.quit()
