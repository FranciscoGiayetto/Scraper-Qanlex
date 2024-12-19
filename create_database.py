import pymysql
from pymysql import MySQLError
from config import DATABASE_CONFIG

def create_database_and_tables():
    """
    Esta función se encarga de crear la base de datos 'expedientes' si no existe,
    y las tablas necesarias dentro de ella: 'details', 'participants', 'actions', 
    'notes', y 'resources'. Además, maneja posibles errores relacionados con la 
    conexión a la base de datos MySQL y los errores de ejecución.

    El proceso sigue estos pasos:
    1. Se conecta al servidor MySQL sin especificar una base de datos inicial.
    2. Se verifica si la base de datos 'expedientes' existe y, si no, se crea.
    3. Se selecciona la base de datos 'expedientes'.
    4. Se crean las tablas necesarias ('details', 'participants', 'actions', 
       'notes' y 'resources') si no existen.
    5. Si ocurre algún error en la conexión o durante la ejecución, se maneja 
       adecuadamente y se muestra un mensaje de error.
    """
    try:
        # Conectar al servidor MySQL sin especificar base de datos
        connection = pymysql.connect(
            host=DATABASE_CONFIG["host"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"]
        )

        with connection.cursor() as cursor:
            # Verificar si la base de datos 'expedientes' ya existe
            cursor.execute("SHOW DATABASES LIKE 'expedientes';")
            result = cursor.fetchone()

            # Si la base de datos no existe, crearla
            if result:
                print("La base de datos 'expedientes' ya existe.")
            else:
                cursor.execute("CREATE DATABASE expedientes;")
                print("Base de datos 'expedientes' creada.")

            # Seleccionar la base de datos 'expedientes'
            cursor.execute("USE expedientes;")

            # Crear la tabla 'details' si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS details (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    dependencia VARCHAR(255),
                    jurisdiccion VARCHAR(255),
                    situacion_actual VARCHAR(255),
                    caratula TEXT,
                    expediente VARCHAR(255)
                );
            """)

            # Crear la tabla 'participants' si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS participants (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tipo VARCHAR(255),
                    nombre TEXT,
                    tomo_folio VARCHAR(255),
                    iej VARCHAR(255),
                    details_id INT,
                    FOREIGN KEY (details_id) REFERENCES details(id) ON DELETE CASCADE
                );
            """)

            # Crear la tabla 'actions' si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS actions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    oficina VARCHAR(255),
                    fecha DATE,
                    tipo VARCHAR(255),
                    detalle TEXT,
                    details_id INT,
                    FOREIGN KEY (details_id) REFERENCES details(id) ON DELETE CASCADE
                );
            """)

            # Crear la tabla 'notes' si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATE,
                    interviniente VARCHAR(255),
                    descripcion TEXT,
                    details_id INT,
                    FOREIGN KEY (details_id) REFERENCES details(id) ON DELETE CASCADE
                );
            """)

            # Crear la tabla 'resources' si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resources (
                    id INT AUTO_INCREMENT PRIMARY KEY,          
                    recurso TEXT,                               
                    oficina_elevacion TEXT,                     
                    fecha_presentacion DATE,                    
                    tipo_recurso TEXT,                          
                    estado_actual TEXT,                         
                    details_id INT,                            
                    FOREIGN KEY (details_id) REFERENCES details(id) ON DELETE CASCADE 
                );
            """)

            # Confirmar los cambios realizados en la base de datos
            connection.commit()

    except MySQLError as err:
        # Manejo de errores específicos de MySQL
        if err.args[0] == 1045:
            print("Acceso denegado: verifique su usuario y contraseña.")
        elif err.args[0] == 1049:
            print("Base de datos no existe.")
        else:
            print(f"Error MySQL: {err}")
    except Exception as e:
        # Manejo de errores generales
        print(f"Ocurrió un error inesperado: {e}")
