import time
from config import setup_driver
from page_interaction import click_header, fill_form_fields, click_search_button, go_to_next_page, click_buttons_in_table
from create_database import create_database_and_tables

# Función para interactuar con la página
def open_page():
    """
    Abre la página web, completa el formulario de búsqueda, procesa los resultados
    y navega a través de las páginas.

    Este proceso incluye:
    - Crear y configurar la base de datos.
    - Interactuar con la página web para completar un formulario con los parámetros necesarios.
    - Procesar las filas de la tabla de resultados y extraer la información.
    - Navegar entre las páginas de resultados si es necesario.

    El flujo general de esta función es:
    1. Crear la base de datos y las tablas necesarias.
    2. Cargar la página web.
    3. Interactuar con los elementos de la página (formularios y botones).
    4. Procesar los resultados y, si es necesario, moverse a la siguiente página.
    """
    # Crear la base de datos y las tablas necesarias
    create_database_and_tables()
    
    # URL de la página a procesar
    url = "http://scw.pjn.gov.ar/scw/home.seam"
    
    # Configurar el driver y cargar la página
    driver = setup_driver()
    driver.get(url)

    # Realizar las interacciones iniciales con la página
    click_header(driver)  # Hacer clic en el encabezado para activar el filtro
    fill_form_fields(driver)  # Llenar los campos del formulario
    time.sleep(20)  # Pausa para que el usuario resuelva el captcha manualmente
    click_search_button(driver)  # Hacer clic en el botón de búsqueda

    # Conjunto para llevar el control de las filas procesadas
    processed_rows = set()
    
    # Bandera para controlar el flujo de la navegación por páginas
    end = True
    
    # Bucle principal para procesar cada página
    while end:
        # Procesar las filas en la página actual
        more_rows_to_process = click_buttons_in_table(driver, processed_rows)
        
        # Si no hay más filas para procesar, se intenta mover a la siguiente página
        if not more_rows_to_process:
            processed_rows = set()  # Reiniciar el conjunto de filas procesadas
            
            # Intentar ir a la siguiente página. Si no es posible, finalizar.
            if not go_to_next_page(driver):
                print("No hay más páginas disponibles.")
                end = False  # Terminar el ciclo si no hay más páginas
    
    # Cerrar el driver al finalizar el proceso
    driver.quit()


# Ejecutar el script cuando el archivo se ejecute directamente
if __name__ == "__main__":
    open_page()
