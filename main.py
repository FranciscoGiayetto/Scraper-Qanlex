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

    time.sleep(5)  # Pausa para el captcha

    click_search_button(driver)

    time.sleep(5)

    processed_rows = set()

    fin = True
    while fin:
        # Procesar filas en la página actual
        more_rows_to_process = click_buttons_in_table(driver, processed_rows)

        # Nos movemos a la siguiente pagina
        if not more_rows_to_process:
            processed_rows = set()
            if not go_to_next_page(driver):
                print("No hay más páginas para procesar. Terminando el script.")
                fin = False

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


# Función para completar los campos Jurisdicción y Parte
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


# Función para hacer clic en el botón de búsqueda después de resolver el captcha
def click_search_button(driver):
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "formPublica:buscarPorParteButton"))
        )
        search_button.click()
        print("Haciendo clic en el botón de búsqueda...")
    except Exception as e:
        print(f"Error al intentar hacer clic en el botón de búsqueda: {e}")


# Ingresar en cada expediente
def click_buttons_in_table(driver, processed_rows):
    try:
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )

        if not rows:
            print("No se encontraron filas.")
            return False

        print(f"Se encontraron {len(rows)} filas. Ingresando...")

        filas_procesadas = 0
        for row_index in range(len(rows)):
            if row_index in processed_rows:
                continue

            try:
                rows = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
                )

                row = rows[row_index]
                buttons = row.find_elements(
                    By.CSS_SELECTOR, "a.btn.btn-default.btn-sm.no-margin"
                )

                if buttons:
                    print(
                        f"Botones encontrados en la fila {row_index+1}: {len(buttons)}"
                    )
                    button = buttons[0]

                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                    button.click()
                    print(f"Haciendo clic en el botón en la fila {row_index+1}...")

                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CLASS_NAME, "btn.btn-default.bg-info")
                        )
                    )
                    back_button.click()
                    print(
                        f"Volviendo a la página de resultados desde la fila {row_index+1}..."
                    )

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "table tr")
                        )
                    )

                    processed_rows.add(row_index)
                    filas_procesadas += 1
                else:
                    print(f"No se encontró un botón en la fila {row_index+1}.")
                    processed_rows.add(row_index)

            except Exception as e:
                print(
                    f"Error al intentar hacer clic en un botón en la fila {row_index+1}: {e}"
                )
                continue

        if filas_procesadas == 0:
            print("No se procesaron filas en este ciclo.")
            return False
        return True

    except Exception as e:
        print(f"Error al intentar hacer clic en los botones: {e}")
        return False


# Avanzar a la siguiente pagina
def go_to_next_page(driver):
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "j_idt118:j_idt208:j_idt215"))
        )
        next_page_button.click()
        print("Yendo a la siguiente página...")

        # Esperar a que las filas de la nueva página sean visibles
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )
        return True
    except Exception as e:
        print(f"Error al intentar ir a la siguiente página: {e}")
        return False


# Ejecutar el script
if __name__ == "__main__":
    open_page()
