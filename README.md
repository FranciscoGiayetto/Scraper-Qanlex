# ⚖️ Scraper de Expedientes Judiciales

Este scraper transforma la búsqueda y gestión de información judicial al automatizar la recolección de datos sobre expedientes relacionados con residuos desde el portal [Sistema de Consulta Web del Poder Judicial de la Nación de Argentina](http://scw.pjn.gov.ar/scw/home.seam). Con esta herramienta, eliminarás la tediosa recolección manual, optimizando tiempo y recursos al estructurar la información directamente en una base de datos MySQL lista para un análisis ágil y preciso. Ideal para quienes buscan eficiencia y fiabilidad en el manejo de grandes volúmenes de datos judiciales.

## ✨ Características Principales

- **Fuente de datos:** Extrae información del portal SCW PJN.
- **Criterios de búsqueda:**
  - Filtra por jurisdicción: "COM".
  - Palabra clave: "residuos".
- **Base de datos:**
  - Creación automática al iniciar el proyecto.
  - Tablas organizadas para detalles, participantes, acciones, notas y recursos asociados a los expedientes.
- **Tecnologías utilizadas:**
  - Python (Selenium y PyMySQL).
  - Base de datos MySQL.

## 🛠️ Tecnologías y Herramientas

- **Lenguaje principal:** Python.
- **Librerías:**
  - `selenium`: Para interactuar con la web.
  - `pymysql`: Para gestionar la base de datos MySQL.
- **Base de datos:** MySQL (configurable en `config.py`).
- **Extras:** ChromeDriver para la navegación automatizada.

## 📋 Requisitos Previos

1. **Python 3.8 instalado.**
2. **MySQL configurado** en tu máquina o servidor.
3. **ChromeDriver instalado** y accesible en tu PATH.

## 🚧 Instalación

1. Clonar el repositorio desde GitHub:
   ```bash
   git clone https://github.com/FranciscoGiayetto/Scraper-Qanlex.git
   cd Scraper-Qanlex
   ```

2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar las credenciales de la base de datos en `config.py`:
   ```python
   DATABASE_CONFIG = {
       "host": "localhost",
       "user": "tu_usuario",
       "password": "tu_contraseña",
       "database": "expedientes"
   }
   ```

## ▶️ Uso

1. Asegúrate de que ChromeDriver esté configurado correctamente.
2. Ejecuta el scraper:
   ```bash
   python3 main.py
   ```
3. Los datos extraídos se almacenarán automáticamente en las tablas de la base de datos MySQL.

## 📂 Estructura de la Base de Datos

- **Details:** Información general del expediente.
- **Participants:** Participantes asociados al expediente.
- **Actions:** Historial de acciones realizadas.
- **Notes:** Notas relacionadas con el expediente.
- **Resources:** Recursos asociados.

## ⚠️ Captchas

- Actualmente, el scraper **no resuelve automáticamente los captchas** presentes en el portal SCW PJN.
- Al detectar un captcha, el script pausa la ejecución durante **20 segundos** para que el usuario lo resuelva manualmente en la ventana del navegador.

## 💡 Posibles Mejoras

Para resolver captchas automáticamente, se pueden integrar servicios externos mediante sus APIs. Algunas opciones son:

1. **[2Captcha](https://2captcha.com/):** Un servicio económico para resolver captchas simples y reCAPTCHA v2/v3.
2. **[Anti-Captcha](https://anti-captcha.com/):** Similar a 2Captcha, con soporte para una amplia variedad de captchas.
3. **[Death By Captcha](http://www.deathbycaptcha.com/):** Otra alternativa popular para resolver captchas.

Integrar cualquiera de estas opciones requeriría:

1. Registrar una cuenta en el servicio seleccionado y obtener una **clave API**.
2. Modificar el script para enviar captchas a la API y manejar las respuestas de forma automática.
3. Gestionar un balance suficiente en la cuenta del servicio para operar sin interrupciones.
