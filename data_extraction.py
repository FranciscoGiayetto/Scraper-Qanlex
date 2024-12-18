from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_notes(driver):
    """
    Extrae los datos de las notas de la página actual.

    Verifica si la tabla de notas está presente y extrae la fecha, el interviniente y 
    la descripción de cada fila en la tabla.

    Args:
        driver: El controlador de Selenium que interactúa con la página.

    Returns:
        list: Una lista de diccionarios con los datos extraídos (fecha, interviniente, descripcion),
              o una lista vacía si no se encuentran notas.
    """
    try:
        notes = []
        
        # Verificar si la tabla de notas está presente
        if len(driver.find_elements(By.ID, "expediente:notas-table")) > 0:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "expediente:notas-table"))
            )
            
            # Obtener todas las filas de la tabla
            rows = table.find_elements(By.XPATH, ".//tbody/tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) >= 3:
                    # Extraer los datos de cada celda
                    fecha = cells[0].text.strip() if len(cells) > 0 else ""
                    interviniente = cells[1].text.strip() if len(cells) > 1 else ""
                    descripcion = cells[2].text.strip() if len(cells) > 2 else ""
                    
                    # Agregar la nota a la lista
                    notes.append(
                        {
                            "fecha": fecha,
                            "interviniente": interviniente,
                            "descripcion": descripcion,
                        }
                    )

            return notes
        else:
            return []

    except Exception as e:
        print(f"Error al extraer notas: {e}")
        return None

def extract_details(driver):
    """
    Extrae los detalles del expediente (dependencia, jurisdicción, situación actual, carátula y expediente).

    Verifica si los elementos correspondientes están presentes y extrae los datos.

    Args:
        driver: El controlador de Selenium que interactúa con la página.

    Returns:
        dict: Un diccionario con los detalles extraídos del expediente.
    """
    try:
        details = {}

        if len(driver.find_elements(By.ID, "expediente:j_idt90:detailDependencia")) > 0:
            department = driver.find_element(By.ID, "expediente:j_idt90:detailDependencia").text
            details["dependencia"] = department

        if len(driver.find_elements(By.ID, "expediente:j_idt90:detailCamera")) > 0:
            jurisdiction = driver.find_element(By.ID, "expediente:j_idt90:detailCamera").text
            details["jurisdiccion"] = jurisdiction

        if len(driver.find_elements(By.ID, "expediente:j_idt90:detailSituation")) > 0:
            current_situation = driver.find_element(By.ID, "expediente:j_idt90:detailSituation").text
            details["situacion_actual"] = current_situation

        if len(driver.find_elements(By.ID, "expediente:j_idt90:detailCover")) > 0:
            cover = driver.find_element(By.ID, "expediente:j_idt90:detailCover").text
            details["caratula"] = cover

        if len(driver.find_elements(By.XPATH, "//label[text()='Expediente:']/following::span[1]")) > 0:
            file = driver.find_element(By.XPATH, "//label[text()='Expediente:']/following::span[1]").text
            details["expediente"] = file

        return details 

    except Exception as e:
        print(f"Error al extraer detalles: {e}")
        return None

def extract_actions(driver):
    """
    Extrae los datos de las actuaciones asociadas al expediente.

    Verifica si la tabla de actuaciones está presente, luego extrae la oficina, fecha, 
    tipo y detalle de cada actuación en la tabla.

    Args:
        driver: El controlador de Selenium que interactúa con la página.

    Returns:
        list: Una lista de diccionarios con los datos extraídos (oficina, fecha, tipo, detalle) 
              de las actuaciones, o una lista vacía si no se encuentran actuaciones.
    """
    actions = []
    try:
        if len(driver.find_elements(By.ID, "expediente:action-table")) > 0:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "expediente:action-table"))
            )
            rows = table.find_elements(By.XPATH, ".//tbody/tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) >= 5:
                    office = cells[1].text.strip()
                    date = cells[2].text.strip()
                    type = cells[3].text.strip()
                    detail = cells[4].text.strip()

                    actions.append(
                        {"oficina": office, "fecha": date, "tipo": type, "detalle": detail}
                    )

        return actions

    except Exception as e:
        print(f"Error al extraer actuaciones: {e}")
        return None

def extract_resources(driver):
    """
    Extrae los datos de los recursos asociados al expediente.

    Primero, se hace clic en el encabezado para expandir la sección de recursos, y luego se extraen 
    los datos de la tabla (recurso, oficina de elevación, fecha de presentación, tipo de recurso, estado).

    Args:
        driver: El controlador de Selenium que interactúa con la página.

    Returns:
        list: Una lista de diccionarios con los datos extraídos (recurso, oficina de elevación, 
              fecha de presentación, tipo de recurso, estado actual), o una lista vacía si no se encuentran recursos.
    """
    header = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "expediente:j_idt371:header:inactive"))
    )
    header.click()
    try:
        if len(driver.find_elements(By.ID, "expediente:recursosTable")) > 0:
            resources = []
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "expediente:recursosTable")
                )
            )
            rows = driver.find_elements(By.XPATH, ".//tbody/tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 5:
                    resource = cells[0].text.strip() if len(cells) > 0 else ""
                    filing_office = cells[1].text.strip() if len(cells) > 1 else ""
                    submission_date = cells[2].text.strip() if len(cells) > 2 else ""
                    resource_type = cells[3].text.strip() if len(cells) > 3 else ""
                    current_status = cells[4].text.strip() if len(cells) > 4 else ""
                    resources.append(
                        {
                            "recurso": resource,
                            "oficina_elevacion": filing_office,
                            "fecha_presentacion": submission_date,
                            "tipo_recurso": resource_type,
                            "estado_actual": current_status,
                        }
                    )
            return resources
    except Exception as e:
        print(f"Error al extraer recursos: {e}")
        return None

def extract_participants(driver):
    """
    Extrae los datos de los participantes y fiscales asociados al expediente.

    Hace clic en el encabezado para expandir la sección de participantes, luego extrae los datos de 
    las tablas de participantes y fiscales, como tipo, nombre, tomo/folio, iej, fiscalía y fiscal.

    Args:
        driver: El controlador de Selenium que interactúa con la página.

    Returns:
        dict: Un diccionario con las listas de participantes y fiscales extraídos.
    """
    try:
        # Hacer clic en el encabezado para expandir la sección de participantes
        header = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "expediente:j_idt261:header:inactive"))
        )
        header.click()

        participants = []
        prosecutors = []

        # Extraer datos de la tabla de participantes
        try:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "expediente:participantsTable"))
            )
            rows = table.find_elements(By.XPATH, ".//tbody/tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) >= 4:
                    # Limpieza del texto de cada celda
                    type = cells[0].text.strip().replace("TIPO :", "") if len(cells) > 0 else ""
                    name = cells[1].text.strip().replace("NOMBRE :", "") if len(cells) > 1 else ""
                    volume_folio = cells[2].text.strip().replace("Tomo :", "").replace("Folio :", "") if len(cells) > 2 else ""
                    iej = cells[3].text.strip() if len(cells) > 3 else ""

                    participants.append(
                        {
                            "tipo": type,
                            "nombre": name,
                            "tomo_folio": volume_folio,
                            "iej": iej,
                        }
                    )
        except Exception as e:
            print(f"Error al extraer participantes: {e}")

        # Extraer datos de la tabla de fiscales
        try:
            if len(driver.find_elements(By.ID, "expediente:fiscalesTable")) > 0:
                prosecutors_table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "expediente:fiscalesTable"))
                )
                prosecutors_rows = prosecutors_table.find_elements(By.XPATH, ".//tbody/tr")

                for row in prosecutors_rows:
                    cells = row.find_elements(By.TAG_NAME, "td")

                    if len(cells) >= 3:
                        # Limpieza del texto de cada celda
                        prosecutor_office = cells[0].text.strip().replace("FISCALÍA :", "") if len(cells) > 0 else ""
                        prosecutor = cells[1].text.strip() if len(cells) > 1 else ""
                        iej = cells[2].text.strip() if len(cells) > 2 else ""

                        prosecutors.append(
                            {
                                "fiscalia": prosecutor_office,
                                "fiscal": prosecutor,
                                "iej": iej,
                            }
                        )

        except Exception as e:
            print(f"Error al extraer fiscales: {e}")

        return {"participantes": participants, "fiscales": prosecutors}

    except Exception as e:
        print(f"Error general al extraer datos: {e}")
        return None
