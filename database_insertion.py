import mysql.connector
from mysql.connector import Error
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_extraction import *


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
    clean_text = raw_date.replace("Fecha:", "").strip()
    try:
        parsed_date = datetime.strptime(clean_text, "%d/%m/%Y")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        print(f"Fecha inválida: {raw_date}")
        return None 

import re

def clean_text(text):
    if text:
        text = text.strip()
        text = re.sub(r'[\n\r\t]+', ' ', text)  
        text = re.sub(r'\s{2,}', ' ', text)     
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
            action["oficina"] = clean_text(action["oficina"]).replace("Oficina:", "") if action.get("oficina") else ""
            action["fecha"] = clean_text(action["fecha"]).replace("Fecha:", "") if action.get("fecha") else ""
            action["tipo"] = clean_text(action["tipo"]).replace("Tipo actuacion:", "") if action.get("tipo") else ""
            action["detalle"] = clean_text(action["detalle"]).replace("Detalle:", "") if action.get("detalle") else ""

            action["fecha"] = clean_date(action["fecha"])

            if action["fecha"]:
                values = (
                    action["oficina"],
                    action["fecha"],
                    action["tipo"],
                    action["detalle"],
                    details_id
                )
                cursor.execute(query, values)

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
            note["fecha"] = clean_text(note["fecha"]).replace("Fecha:", "") if note.get("fecha") else ""
            note["interviniente"] = clean_text(note["interviniente"]).replace("Interviniente:", "") if note.get("interviniente") else ""
            note["descripcion"] = clean_text(note["descripcion"]).replace("Descripción:", "") if note.get("descripcion") else ""

            note["fecha"] = clean_date(note["fecha"])

            if note["fecha"]:
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


def insert_resources(connection, resources, details_id):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO resources (recurso, oficina_elevacion, fecha_presentacion, tipo_recurso, estado_actual, details_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        for resource in resources:
            resource["recurso"] = clean_text(resource["recurso"]).replace("Recurso:", "") if resource.get("recurso") else ""
            resource["oficina_elevacion"] = clean_text(resource["oficina_elevacion"]).replace("Oficina de elevación:", "") if resource.get("oficina_elevacion") else ""
            resource["fecha_presentacion"] = clean_text(resource["fecha_presentacion"]).replace("Fecha de presentación:", "") if resource.get("fecha_presentacion") else ""
            resource["tipo_recurso"] = clean_text(resource["tipo_recurso"]).replace("Tipo de recurso:", "") if resource.get("tipo_recurso") else ""
            resource["estado_actual"] = clean_text(resource["estado_actual"]).replace("Estado actual:", "") if resource.get("estado_actual") else ""

            resource["fecha_presentacion"] = clean_date(resource["fecha_presentacion"])

            if resource["fecha_presentacion"]:
                values = (
                    resource["recurso"],
                    resource["oficina_elevacion"],
                    resource["fecha_presentacion"],
                    resource["tipo_recurso"],
                    resource["estado_actual"],
                    details_id
                )
                cursor.execute(query, values)

        connection.commit()
    except Error as e:
        print(f"Error al insertar recursos: {e}")
