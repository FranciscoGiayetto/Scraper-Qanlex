import mysql.connector
from mysql.connector import Error
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_extraction import *  # Importa funciones de extracción de datos

# Función para insertar los detalles extraídos en la base de datos
def insert_details(connection, details):
    """
    Inserta los detalles extraídos en la tabla 'details' de la base de datos.

    Parámetros:
        connection (mysql.connector.connection): Conexión activa a la base de datos.
        details (dict): Diccionario que contiene los detalles extraídos que se insertarán en la tabla.
            Claves esperadas: 'dependencia', 'jurisdiccion', 'situacion_actual', 'caratula', 'expediente'.

    Retorna:
        int: El ID del registro insertado en la tabla 'details'. Si ocurre un error, retorna None.
    """
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
        return cursor.lastrowid  # Retorna el ID del registro insertado
    except Error as e:
        print(f"Error al insertar detalles: {e}")
        return None


# Función para insertar participantes en la base de datos
def insert_participants(connection, participants, details_id):
    """
    Inserta los participantes extraídos en la tabla 'participants' de la base de datos.

    Parámetros:
        connection (mysql.connector.connection): Conexión activa a la base de datos.
        participants (dict): Diccionario que contiene una lista de participantes a insertar.
            La clave 'participantes' debe contener una lista de diccionarios con las claves 'tipo', 'nombre', 'tomo_folio', 'iej'.
        details_id (int): ID del registro en la tabla 'details' con el que se relacionan los participantes.

    Retorna:
        None
    """
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
                details_id  # Relaciona los participantes con el detalle mediante details_id
            )
            cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"Error al insertar participantes: {e}")


from datetime import datetime

# Función para limpiar y convertir la fecha a formato YYYY-MM-DD
def clean_date(raw_date):
    """
    Limpia y convierte una fecha en formato 'DD/MM/YYYY' a 'YYYY-MM-DD'.

    Parámetros:
        raw_date (str): Fecha en formato 'DD/MM/YYYY' que se desea convertir.

    Retorna:
        str: Fecha convertida en formato 'YYYY-MM-DD'. Si la fecha no es válida, retorna None.
    """
    clean_text = raw_date.replace("Fecha:", "").strip()
    try:
        parsed_date = datetime.strptime(clean_text, "%d/%m/%Y")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        print(f"Fecha inválida: {raw_date}")
        return None  # Retorna None si no se puede convertir la fecha


import re

# Función para limpiar el texto de los campos
def clean_text(text):
    """
    Limpia el texto de un campo eliminando espacios en blanco innecesarios y saltos de línea.

    Parámetros:
        text (str): Texto que se desea limpiar.

    Retorna:
        str: Texto limpio, con saltos de línea y espacios múltiples eliminados.
    """
    if text:
        text = text.strip()
        text = re.sub(r'[\n\r\t]+', ' ', text)  # Elimina saltos de línea y tabulaciones
        text = re.sub(r'\s{2,}', ' ', text)  # Reemplaza múltiples espacios por uno solo
        return text
    return ""


# Función para insertar las actuaciones en la base de datos
def insert_actions(connection, actions, details_id):
    """
    Inserta las actuaciones extraídas en la tabla 'actions' de la base de datos.

    Parámetros:
        connection (mysql.connector.connection): Conexión activa a la base de datos.
        actions (list): Lista de diccionarios con las actuaciones extraídas.
            Cada diccionario debe contener las claves: 'oficina', 'fecha', 'tipo', 'detalle'.
        details_id (int): ID del registro en la tabla 'details' con el que se relacionan las actuaciones.

    Retorna:
        None
    """
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

            # Limpiar y convertir la fecha
            action["fecha"] = clean_date(action["fecha"])

            if action["fecha"]:  # Si la fecha es válida, insertar la acción
                values = (
                    action["oficina"],
                    action["fecha"],
                    action["tipo"],
                    action["detalle"],
                    details_id  # Relacionar la acción con el detalle
                )
                cursor.execute(query, values)

        connection.commit()
    except Error as e:
        print(f"Error al insertar actuaciones: {e}")


# Función para insertar las notas en la base de datos
def insert_notes(connection, notes, details_id):
    """
    Inserta las notas extraídas en la tabla 'notes' de la base de datos.

    Parámetros:
        connection (mysql.connector.connection): Conexión activa a la base de datos.
        notes (list): Lista de diccionarios con las notas extraídas.
            Cada diccionario debe contener las claves: 'fecha', 'interviniente', 'descripcion'.
        details_id (int): ID del registro en la tabla 'details' con el que se relacionan las notas.

    Retorna:
        None
    """
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

            # Limpiar y convertir la fecha
            note["fecha"] = clean_date(note["fecha"])

            if note["fecha"]:  # Si la fecha es válida, insertar la nota
                values = (
                    note["fecha"],
                    note["interviniente"],
                    note["descripcion"],
                    details_id  # Relacionar la nota con el detalle
                )
                cursor.execute(query, values)

        connection.commit()
    except Error as e:
        print(f"Error al insertar notas: {e}")


# Función para insertar recursos en la base de datos
def insert_resources(connection, resources, details_id):
    """
    Inserta los recursos extraídos en la tabla 'resources' de la base de datos.

    Parámetros:
        connection (mysql.connector.connection): Conexión activa a la base de datos.
        resources (list): Lista de diccionarios con los recursos extraídos.
            Cada diccionario debe contener las claves: 'recurso', 'oficina_elevacion', 'fecha_presentacion',
            'tipo_recurso', 'estado_actual'.
        details_id (int): ID del registro en la tabla 'details' con el que se relacionan los recursos.

    Retorna:
        None
    """
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

            # Limpiar y convertir la fecha de presentación
            resource["fecha_presentacion"] = clean_date(resource["fecha_presentacion"])

            if resource["fecha_presentacion"]:  # Si la fecha es válida, insertar el recurso
                values = (
                    resource["recurso"],
                    resource["oficina_elevacion"],
                    resource["fecha_presentacion"],
                    resource["tipo_recurso"],
                    resource["estado_actual"],
                    details_id  # Relacionar el recurso con el detalle
                )
                cursor.execute(query, values)

        connection.commit()
    except Error as e:
        print(f"Error al insertar recursos: {e}")
