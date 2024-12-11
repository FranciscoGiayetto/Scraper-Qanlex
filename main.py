from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Configuración de Selenium
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver


# Función para interactuar con la página
def open_page():
    url = "http://scw.pjn.gov.ar/scw/home.seam"
    driver = setup_driver()
    driver.get(url)

    # Hacer clic en el header de "Por parte"
    click_por_parte(driver)

    time.sleep(5)

    driver.quit()


# Funcion para cambiar a por parte
def click_por_parte(driver):
    try:
        por_parte_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "formPublica:porParte:header:inactive"))
        )
        por_parte_tab.click()
        print('Haciendo clic en "Por parte"...')
    except Exception as e:
        print(f"Error al intentar hacer clic en 'Por parte': {e}")


# Ejecutar el script
if __name__ == "__main__":
    open_page()
