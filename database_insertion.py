import mysql.connector
from mysql.connector import Error
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_extraction import *

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="tu_usuario",
            password="tu_contraseña",
            database="expedientes"
        )
        return connection
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None

def insert_details(connection, details):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO details (dependencia, jurisdiccion, situacion_actual, caratula, expediente)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            details["dependencia"],
            details["jurisdiccion"],
            details["situacion_actual"],
            details["caratula"],
            details["expediente"]
        )
        cursor.execute(query, values)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error al insertar detalles: {e}")
        return None

def insert_participants(connection, participants, details_id):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO participants (tipo, nombre, tomo_folio, iej, details_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        for participant in participants["participantes"]:
            values = (
                participant["tipo"],
                participant["nombre"],
                participant["tomo_folio"],
                participant["iej"],
                details_id
            )
            cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"Error al insertar participantes: {e}")

from datetime import datetime

def clean_date(raw_date):
    # Elimina el prefijo "Fecha:\n" y espacios innecesarios
    clean_text = raw_date.replace("Fecha:", "").strip()
    try:
        # Convierte al formato 'YYYY-MM-DD'
        parsed_date = datetime.strptime(clean_text, "%d/%m/%Y")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        print(f"Fecha inválida: {raw_date}")
        return None  # O manejarlo como prefieras

import re

def clean_text(text):
    """Limpia el texto eliminando caracteres no deseados."""
    if text:
        # Elimina saltos de línea, espacios adicionales y caracteres no imprimibles
        text = text.strip()
        text = re.sub(r'[\n\r\t]+', ' ', text)  # Reemplaza saltos de línea y tabs por un solo espacio
        text = re.sub(r'\s{2,}', ' ', text)     # Reemplaza múltiples espacios por uno solo
        return text
    return ""

def insert_actions(connection, actions, details_id):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO actions (oficina, fecha, tipo, detalle, details_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        for action in actions:
            # Limpieza de los campos de la acción antes de la inserción
            action["oficina"] = clean_text(action["oficina"]).replace("Oficina:", "") if action.get("oficina") else ""
            action["fecha"] = clean_text(action["fecha"]).replace("Fecha:", "") if action.get("fecha") else ""
            action["tipo"] = clean_text(action["tipo"]).replace("Tipo actuacion:", "") if action.get("tipo") else ""
            action["detalle"] = clean_text(action["detalle"]).replace("Detalle:", "") if action.get("detalle") else ""

            # Limpia y valida la fecha
            action["fecha"] = clean_date(action["fecha"])

            # Verifica que la fecha sea válida antes de insertar
            if action["fecha"]:
                values = (
                    action["oficina"],
                    action["fecha"],
                    action["tipo"],
                    action["detalle"],
                    details_id
                )
                cursor.execute(query, values)
            else:
                print(f"Actuación omitida por fecha inválida: {action}")

        connection.commit()
    except Error as e:
        print(f"Error al insertar actuaciones: {e}")

        
def insert_notes(connection, notes, details_id):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO notes (fecha, interviniente, descripcion, details_id)
        VALUES (%s, %s, %s, %s)
        """
        for note in notes:
            values = (
                note["fecha"],
                note["interviniente"],
                note["descripcion"],
                details_id
            )
            cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"Error al insertar notas: {e}")

def extract_and_store_data(driver):
    connection = connect_to_db()
    if connection is None:
        return

    try:
        # Extraer detalles
        details = extract_details(driver)
        details_id = insert_details(connection, details)

        if details_id is None:
            return

        # Extraer participantes
        participants = extract_participants(driver)
        insert_participants(connection, participants, details_id)

        # Extraer actuaciones
        actions = extract_actions(driver)
        insert_actions(connection, actions, details_id)

        # Extraer notas
        notes = extract_notes(driver)
        insert_notes(connection, notes, details_id)

        print("Datos almacenados correctamente.")
    finally:
        connection.close()

