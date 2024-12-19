from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from data_extraction import *  # Importa funciones que extraen datos de la página web
from database_insertion import *  # Importa funciones que insertan datos en la base de datos
import pymysql
from config import DATABASE_CONFIG  # Carga la configuración de la base de datos desde un archivo de configuración
from selenium.common.exceptions import StaleElementReferenceException  # Excepción que puede ocurrir si un elemento se vuelve obsoleto


# Función para cambiar a la pestaña "Por parte"
def click_header(driver):
    try:
        # Espera hasta que el tab "Por parte" sea clickeable y hace clic en él
        por_parte_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "formPublica:porParte:header:inactive"))
        )
        por_parte_tab.click()  # Hace clic en la pestaña
    except Exception as e:
        # Si ocurre un error (por ejemplo, el elemento no es encontrado), lo captura y lo imprime
        print(f"Error al intentar hacer clic en header: {e}")


# Función para completar los campos "Jurisdicción" y "Parte" en el formulario
def fill_form_fields(driver):
    try:
        # Espera a que el campo "Jurisdicción" esté presente y lo completa con el valor "COM"
        jurisdiccion_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formPublica:camaraPartes"))
        )
        jurisdiccion_input.send_keys("COM")

        # Espera a que el campo "Parte" esté presente y lo completa con el valor "RESIDUOS"
        parte_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formPublica:nomIntervParte"))
        )
        parte_input.send_keys("RESIDUOS")

    except Exception as e:
        # Si ocurre un error al completar los campos, lo captura y lo imprime
        print(f"Error al intentar completar los campos: {e}")


# Función para hacer clic en el botón de búsqueda después de resolver el captcha
def click_search_button(driver):
    try:
        # Espera hasta que el botón de búsqueda sea clickeable y hace clic en él
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "formPublica:buscarPorParteButton"))
        )
        search_button.click()  # Realiza la acción de hacer clic en el botón de búsqueda
    except Exception as e:
        # Si ocurre un error al intentar hacer clic, lo captura y lo imprime
        print(f"Error al intentar hacer clic en el botón de búsqueda: {e}")


# Función que recorre las filas de la tabla, procesando cada expediente
def click_buttons_in_table(driver, processed_rows):
    try:
        # Espera hasta que todas las filas de la tabla estén presentes
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )

        # Si no hay filas en la tabla, retorna False
        if not rows:
            return False

        # Establece una conexión a la base de datos para insertar los datos extraídos
        connection = pymysql.connect(**DATABASE_CONFIG)

        # Itera sobre las filas de la tabla para procesar los expedientes
        for row_index, row in enumerate(rows):
            # Si la fila ya fue procesada, la salta
            if row_index in processed_rows:
                continue

            try:
                # Asegura que las filas actuales estén actualizadas (puede cambiar dinámicamente)
                rows = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
                )
                row = rows[row_index]

                # Encuentra los botones dentro de la fila para poder hacer clic
                buttons = row.find_elements(
                    By.CSS_SELECTOR, "a.btn.btn-default.btn-sm.no-margin"
                )
                if buttons:
                    # Si hay botones, toma el primero y espera a que sea clickeable
                    button = buttons[0]
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                    button.click()  # Hace clic en el botón

                    # Llama a las funciones para extraer los datos de la página
                    actions = extract_actions(driver)
                    notes = extract_notes(driver)
                    details = extract_details(driver)
                    participants = extract_participants(driver)
                    resources = extract_resources(driver)

                    # Inserta los datos extraídos en la base de datos
                    details_id = insert_details(connection, details)
                    insert_participants(connection, participants, details_id)
                    insert_actions(connection, actions, details_id)

                    # Inserta notas si existen
                    if notes is not None:
                        insert_notes(connection, notes, details_id)
                    # Inserta recursos si existen
                    if resources is not None:
                        insert_resources(connection, resources, details_id)
                    
                    # Vuelve a la tabla después de procesar un expediente
                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CLASS_NAME, "btn.btn-default.bg-info")
                        )
                    )
                    back_button.click()  # Hace clic en el botón para regresar a la tabla

                    # Espera a que la tabla esté presente nuevamente
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "table tr")
                        )
                    )

                    # Marca esta fila como procesada
                    processed_rows.add(row_index)
                else:
                    # Si no se encuentra un botón, marca la fila como procesada
                    processed_rows.add(row_index)
            except StaleElementReferenceException as e:
                continue
            except Exception as e:
                # Captura otros errores y los imprime
                print(f"Error en la fila {row_index + 1}: {e}")
                continue

        return  # Termina el procesamiento

    except Exception as e:
        # Si ocurre un error al procesar la tabla, lo captura y lo imprime
        print(f"Error al procesar la tabla: {e}")
        return False


# Función para avanzar a la siguiente página de resultados en la tabla
def go_to_next_page(driver):
    try:
        # Espera hasta que el botón "Siguiente" sea clickeable y hace clic en él
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "j_idt118:j_idt208:j_idt215"))
        )

        next_page_button.click()  # Hace clic en el botón "Siguiente"

        # Espera a que las filas de la siguiente página estén disponibles
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )
        return True  # Indica que se avanzó correctamente a la siguiente página
    except Exception as e:
        # Si ocurre un error, captura y retorna False
        return False
