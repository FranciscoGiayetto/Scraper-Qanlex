import time
from config import setup_driver
from page_interaction import click_header,fill_form_fields,click_search_button,go_to_next_page,click_buttons_in_table
from create_database import create_database_and_tables

# Función para interactuar con la página
def open_page():
    create_database_and_tables()
    url = "http://scw.pjn.gov.ar/scw/home.seam"
    driver = setup_driver()
    driver.get(url)

    click_header(driver)
    fill_form_fields(driver)
    time.sleep(20)  # Pausa para el captcha
    click_search_button(driver)

    processed_rows = set()
    end = True
    while end:
        # Procesar filas en la página actual
        more_rows_to_process = click_buttons_in_table(driver, processed_rows)
        # Nos movemos a la siguiente pagina
        if not more_rows_to_process:
            processed_rows = set()
            if not go_to_next_page(driver):
                print("No hay más páginas disponibles.")
                end = False
    driver.quit()


# Ejecutar el script
if __name__ == "__main__":
    open_page()
