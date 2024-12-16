from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuración de Selenium
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Especifica la ubicación del binario de Google Chrome
    options.binary_location = "/usr/bin/google-chrome"

    # Usa ChromeDriverManager para manejar la instalación de ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Inicia el driver con la configuración del service y las opciones
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Configuración de la base de datos
DATABASE_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "pepe1234",
    "database": "expedientes",
    "port": 3306,
    "connect_timeout": 10,
}

