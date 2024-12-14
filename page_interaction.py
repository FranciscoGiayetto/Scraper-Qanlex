from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from data_extraction import *
from database_insertion import *
import pymysql
from config import DATABASE_CONFIG


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
        jurisdiccion_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formPublica:camaraPartes"))
        )
        jurisdiccion_input.send_keys("COM")

        parte_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formPublica:nomIntervParte"))
        )
        parte_input.send_keys("RESIDUOS")

    except Exception as e:
        print(f"Error al intentar completar los campos: {e}")


# Función para hacer clic en el botón de búsqueda después de resolver el captcha
def click_search_button(driver):
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "formPublica:buscarPorParteButton"))
        )
        search_button.click()
    except Exception as e:
        print(f"Error al intentar hacer clic en el botón de búsqueda: {e}")


# Ingresar en cada expediente
def click_buttons_in_table(driver, processed_rows):
    try:
        # Reobtén las filas de la tabla en cada iteración
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )

        if not rows:
            return False

        connection = pymysql.connect(**DATABASE_CONFIG)

        for row_index, row in enumerate(rows):
            if row_index in processed_rows:
                continue

            try:

                # Vuelve a obtener las filas para evitar referencias obsoletas
                rows = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
                )
                row = rows[row_index]

                buttons = row.find_elements(
                    By.CSS_SELECTOR, "a.btn.btn-default.btn-sm.no-margin"
                )
                if buttons:
                    button = buttons[0]
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                    button.click()

                    # Extracción de datos
                    notes = extract_notes(driver)
                    actions = extract_actions(driver)
                    details = extract_details(driver)
                    participants = extract_participants(driver)
                    resources = extract_resources(driver)

                    # # # Insertar datos en la base de datos
                    details_id = insert_details(connection, details)
                    insert_participants(connection, participants, details_id)
                    insert_actions(connection, actions, details_id)
                    # insert_notes(connection, notes, details_id)
                    
                    # Volver a la tabla
                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CLASS_NAME, "btn.btn-default.bg-info")
                        )
                    )
                    back_button.click()

                    # Esperar a que la tabla se recargue
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "table tr")
                        )
                    )

                    processed_rows.add(row_index)
                else:
                    processed_rows.add(row_index)

            except Exception as e:
                print(f"Error en la fila {row_index + 1}: {e}")
                continue

        return 

    except Exception as e:
        print(f"Error al procesar la tabla: {e}")
        return False


# Avanzar a la siguiente pagina
def go_to_next_page(driver):
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "j_idt118:j_idt208:j_idt215"))
        )
        next_page_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )
        return True
    except Exception as e:
        print(f"Error al intentar ir a la siguiente página: {e}")
        return False
