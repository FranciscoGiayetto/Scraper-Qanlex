import pymysql
from pymysql import MySQLError
from config import DATABASE_CONFIG

def create_database_and_tables():
    try:
        # Conectar al servidor MySQL sin especificar base de datos (para crearla si no existe)
        connection = pymysql.connect(
            host=DATABASE_CONFIG["host"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"]
        )

        with connection.cursor() as cursor:
            # Verificar si la base de datos ya existe
            cursor.execute("SHOW DATABASES LIKE 'expedientes';")
            result = cursor.fetchone()

            # Si la base de datos no existe, crearla
            if result:
                print("La base de datos 'expedientes' ya existe.")
            else:
                cursor.execute("CREATE DATABASE expedientes;")
                print("Base de datos 'expedientes' creada.")

            # Usar la base de datos
            cursor.execute("USE expedientes;")

            # Crear las tablas si no existen
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

            # Confirmar los cambios
            connection.commit()
            print("Las tablas se han creado (si no existían).")

    except MySQLError as err:
        if err.args[0] == 1045:
            print("Acceso denegado: verifique su usuario y contraseña.")
        elif err.args[0] == 1049:
            print("Base de datos no existe.")
        else:
            print(f"Error MySQL: {err}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

