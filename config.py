from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# Configuración de Selenium
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
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

