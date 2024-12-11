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

    click_header(driver)

    fill_form_fields(driver)

    time.sleep(5)

    driver.quit()


# Función para cambiar a "Por parte"
def click_header(driver):
    try:
        por_parte_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "formPublica:porParte:header:inactive"))
        )
        por_parte_tab.click()
    except Exception as e:
        print(f"Error al intentar hacer clic en header: {e}")


# Función para completar los campos Jurisdicción y "Parte
def fill_form_fields(driver):
    try:
        camara_partes_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formPublica:camaraPartes"))
        )
        camara_partes_input.send_keys("COM")

        nom_interv_parte_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formPublica:nomIntervParte"))
        )
        nom_interv_parte_input.send_keys("RESIDUOS")

        print('Campos completados: "Jurisdicción" y "Parte"')
    except Exception as e:
        print(f"Error al intentar completar los campos: {e}")


# Ejecutar el script
if __name__ == "__main__":
    open_page()
