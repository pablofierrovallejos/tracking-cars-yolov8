import pymysql
import aiomysql
import asyncio


from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)



def connect_to_mysql():
    """
    Establece una conexión con la base de datos MySQL.
    :return: Objeto de conexión si es exitosa, None de lo contrario.
    """
    try:
        connection = pymysql.connect(
            host="localhost",  # Reemplazar por la dirección de tu servidor MySQL
            user="root",  # Reemplazar por tu usuario de MySQL
            password="sasa",  # Reemplazar por tu contraseña de MySQL
            database="traking"  # Reemplazar por tu base de datos
        )
        print("Conexión exitosa a MySQL.")
        return connection
    except Exception as e:
        print("Error al conectarse a MySQL:", e)
        return None


async def add_record_to_mysql_async(connection, table_name, record):
    """
    Agrega un registro a una tabla en MySQL.
    :param connection: Objeto de conexión a MySQL.
    :param table_name: Nombre de la tabla donde se insertará el registro.
    :param record: Diccionario con los datos del registro.
    """
    try:

        # Lógica para conectar y escribir en la base de datos MySQL de forma asíncrona
        # Esto usa aiomysql
        conn = await aiomysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sasa",
            db="traking",
        )

        # Crear la consulta para insertar datos dinámicamente
        columns = ", ".join(record.keys())
        placeholders = ", ".join(["%s"] * len(record))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(query)

        async with conn.cursor() as cursor:

            await cursor.execute(query, tuple(record.values()))
            await conn.commit()
        print(f"Registro insertado en la tabla {table_name} con éxito.")
        return True  # Retorna algo significativo si es necesario


    except Exception as e:
        print("Error al agregar el registro a MySQL:", e)
        connection.rollback()  # Revertir cambios en caso de error
    finally:
        conn.close()  # Conexión cerrada manualmente


async def add_registro_mysql_async(connection, table_name, datos):
    """
    Función asíncrona para insertar un registro en la base de datos MySQL.
    """
    try:
        # Asume que ya existe la función `add_record_to_mysql_async` para inserción asíncrona.
        await add_record_to_mysql_async(connection, table_name, datos)
    except Exception as e:
        print(f"Error al insertar registro de manera asíncrona: {e}")


def add_registro_mysql(mijsonreg):
    """
    Función llamada desde `predict.py`, delega la inserción a una tarea asíncrona
    y libera el flujo principal.
    """
    table_name = "mitrack"  # Cambiar por el nombre de tu tabla
    connection = connect_to_mysql()


    try:

        # Verifica si hay un bucle de eventos en ejecución
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Si ya hay un bucle de eventos, programa la tarea

             # Lanza la tarea asíncrona en segundo plano.
            asyncio.create_task(add_registro_mysql_async(connection, table_name,mijsonreg))
        else:
            # Si no hay un bucle activo, créalo y ejecútalo
            loop.run_until_complete(add_registro_mysql_async(connection, table_name,mijsonreg))

    except Exception as e:
        print(f"Error al programar la tarea asíncrona: {e}")







def add_record_to_mysql(record):
    """
    Agrega un registro a una tabla en MySQL.

    :param connection: Objeto de conexión a MySQL.
    :param table_name: Nombre de la tabla donde se insertará el registro.
    :param record: Diccionario con los datos del registro.
    """
    try:
        table_name = "mitrack"  # Cambiar por el nombre de tu tabla
        connection = connect_to_mysql()


        # Crear el cursor para ejecutar las consultas
        cursor = connection.cursor()

        # Crear la consulta para insertar datos dinámicamente
        columns = ", ".join(record.keys())
        placeholders = ", ".join(["%s"] * len(record))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Ejecutar la consulta
        cursor.execute(query, tuple(record.values()))

        # Confirmar la transacción
        connection.commit()
        print(f"Registro insertado en la tabla {table_name} con éxito.")
    except Exception as e:
        print("Error al agregar el registro a MySQL:", e)
        connection.rollback()  # Revertir cambios en caso de error
    finally:
        #cursor.close()
        connection.close()




def insert_data_sync(datos):
    """
    Inserta datos en la base de datos de forma síncrona.
    """
    try:
        add_record_to_mysql(datos)  # Versión síncrona de la función
        #print(f"Registro insertado en la base de datos: {datos[:300]}")
    except Exception as e:
        print(f"Error al insertar de forma síncrona: {e}")



def schedule_insertion_thread(mijsonreg):
    """
    Encola la tarea de inserción en un hilo separado.
    """
    executor.submit(insert_data_sync, mijsonreg)
    print("Inserción programada en un hilo separado.")

