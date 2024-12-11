from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Extraer datos de las notas
def extract_notes(driver):
    try:
        notes = []

        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//table/thead//th[contains(text(),'FECHA')]")
            )
        )
        rows = driver.find_elements(By.XPATH, ".//tbody/tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 3:
                fecha = cells[0].text.strip() if len(cells) > 0 else ""
                interviniente = cells[1].text.strip() if len(cells) > 1 else ""
                descripcion = cells[2].text.strip() if len(cells) > 2 else ""

                notes.append(
                    {
                        "fecha": fecha,
                        "interviniente": interviniente,
                        "descripcion": descripcion,
                    }
                )

        return notes

    except Exception as e:
        print(f"Error al extraer notas: {e}")
        return None


# Extraer datos generales
def extract_details(driver):
    try:
        details = {}

        department = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.ID, "expediente:j_idt90:detailDependencia")
                )
            )
            .text
        )
        details["dependencia"] = department

        jurisdiction = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.ID, "expediente:j_idt90:detailCamera")
                )
            )
            .text
        )
        details["jurisdiccion"] = jurisdiction

        current_situation = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.ID, "expediente:j_idt90:detailSituation")
                )
            )
            .text
        )
        details["situacion_actual"] = current_situation

        cover = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.ID, "expediente:j_idt90:detailCover")
                )
            )
            .text
        )
        details["caratula"] = cover

        file = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, "//label[text()='Expediente:']/following::span[1]")
                )
            )
            .text
        )
        details["expediente"] = file

        return details

    except Exception as e:
        print(f"Error al extraer detalles: {e}")
        return None


# Extraer datos de actuaciones
def extract_actions(driver):
    try:
        actions = []

        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "expediente:action-table"))
        )
        rows = table.find_elements(By.XPATH, ".//tbody/tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 5:
                office = cells[1].text.strip() if len(cells) > 1 else ""
                date = cells[2].text.strip() if len(cells) > 2 else ""
                type = cells[3].text.strip() if len(cells) > 3 else ""
                detail = cells[4].text.strip() if len(cells) > 4 else ""

                actions.append(
                    {"oficina": office, "fecha": date, "tipo": type, "detalle": detail}
                )

        return actions

    except Exception as e:
        print(f"Error al extraer actuaciones: {e}")
        return None


# Extraer datos de los recursos
def extract_resources(driver):
    header = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "expediente:j_idt371:header:inactive"))
    )
    header.click()
    try:
        resources = []
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//table/thead//th[contains(text(),'Recurso')]")
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


# Extraer el dato de los participantes
def extract_participants(driver):
    header = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "expediente:j_idt261:header:inactive"))
    )
    header.click()
    try:
        participants = []
        prosecutors = []
        try:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "expediente:participantsTable"))
            )
            rows = table.find_elements(By.XPATH, ".//tbody/tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) >= 4:
                    type = cells[0].text.strip() if len(cells) > 0 else ""
                    name = cells[1].text.strip() if len(cells) > 1 else ""
                    volume_folio = cells[2].text.strip() if len(cells) > 2 else ""
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

        try:
            prosecutors_table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "expediente:fiscalesTable"))
            )
            prosecutors_rows = prosecutors_table.find_elements(By.XPATH, ".//tbody/tr")

            for row in prosecutors_rows:
                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) >= 3:
                    prosecutor_office = cells[0].text.strip() if len(cells) > 0 else ""
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
