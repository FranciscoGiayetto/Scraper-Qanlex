from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuración de Selenium
def setup_driver():
    """
    Configura y devuelve una instancia de Selenium WebDriver para Chrome.

    Esta función configura el entorno de Selenium para utilizar Google Chrome. 
    Ajusta algunas opciones para optimizar el uso en contenedores y entornos de servidor. 
    También maneja la instalación de ChromeDriver utilizando el gestor de WebDriver 
    de ChromeDriverManager.

    Args:
        None

    Returns:
        webdriver.Chrome: Instancia de WebDriver configurada y lista para usar.

    Raises:
        WebDriverException: Si hay un problema al configurar el WebDriver.
    """
    # Crear una instancia de las opciones de Chrome
    options = webdriver.ChromeOptions()

    # Configura opciones para evitar problemas en entornos limitados (como contenedores)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Especifica la ubicación del binario de Google Chrome (importante para servidores)
    options.binary_location = "/usr/bin/google-chrome"

    # Usa ChromeDriverManager para descargar e instalar el ChromeDriver necesario
    service = Service(ChromeDriverManager().install())

    # Inicia el WebDriver de Chrome con las opciones y el servicio configurado
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


# Configuración de la base de datos
DATABASE_CONFIG = {
    "host": "127.0.0.1",        # Dirección IP del servidor de base de datos
    "user": "root",             # Usuario para acceder a la base de datos
    "password": "*****",     # Contraseña del usuario de la base de datos
    "database": "expedientes",  # Nombre de la base de datos a utilizar
    "port": 3306,               # Puerto de conexión de la base de datos (por defecto 3306)
    "connect_timeout": 10,      # Tiempo máximo de espera para establecer la conexión
}
