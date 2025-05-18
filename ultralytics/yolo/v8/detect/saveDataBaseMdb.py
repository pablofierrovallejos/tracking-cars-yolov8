from pymongo import MongoClient
import pymysql
import aiomysql

import asyncio



def connect_to_mongodb():
    try:
        # URL de conexión a MongoDB
        connection_string = "mongodb://localhost:27017/"

        # Crear un cliente para conectarse a MongoDB
        client = MongoClient(connection_string)

        # Verificar la conexión listando las bases de datos disponibles
        databases = client.list_database_names()
        print("Conexión exitosa a MongoDB.")
        print("Bases de datos disponibles:", databases)

        # Retornar el cliente para realizar operaciones posteriores
        return client
    except Exception as e:
        print("Error al conectarse a MongoDB:", e)
        return None


def add_record_to_db(client, database_name, collection_name, record):
    """
    Agrega un registro a una colección en una base de datos específica.

    :param client: Cliente de conexión a MongoDB.
    :param database_name: Nombre de la base de datos.
    :param collection_name: Nombre de la colección.
    :param record: Diccionario con los datos a insertar.
    """
    try:
        # Acceder a la base de datos
        db = client[database_name]

        # Acceder a la colección
        collection = db[collection_name]

        # Insertar el registro
        result = collection.insert_one(record)
        print(f"Registro insertado con ID: {result.inserted_id}")
    except Exception as e:
        print("Error al agregar el registro a la base de datos:", e)



def add_registro(mijsonreg):
    database_name = "traking"  # Reemplazar con el nombre real de la base de datos
    collection_name = "mitrack"  # Reemplazar con el nombre real de la colección


    client = connect_to_mongodb()
    add_record_to_db(client, database_name, collection_name, mijsonreg)
    client.close()

# Llamar a la función para conectarse y agregar un registro de ejemplo
if __name__ == "__main__":
    client = connect_to_mongodb()

    if client:
        try:
            # Parámetros de ejemplo
            database_name = "traking"  # Reemplazar con el nombre real de la base de datos
            collection_name = "mitrack"  # Reemplazar con el nombre real de la colección
            record = {"nombre": "Juan", "edad": 30, "ciudad": "Madrid"}  # Registro de ejemplo

            # Agregar el registro
            add_record_to_db(client, database_name, collection_name, record)
        finally:
            # Cerramos la conexión al terminar
            client.close()







def connect_to_mysql():
    """
    Establece una conexión con la base de datos MySQL.

    :return: Objeto de conexión si es exitosa, None de lo contrario.
    """
    try:
        # Datos de conexión (cambiar según tus configuraciones)
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

async def connect_to_mysql_async(host: str, user: str, password: str, db: str):
    """Establece una conexión asíncrona con MySQL."""
    connection = await aiomysql.connect(host=host, user=user, password=password, db=db)
    return connection


async def add_record_to_mysql_async(host: str, user: str, password: str, db: str, query: str, values: tuple):
    """Inserta un registro en MySQL de forma asíncrona."""
    connection = await connect_to_mysql_async(host, user, password, db)
    async with connection.cursor() as cursor:
        await cursor.execute(query, values)
        await connection.commit()
    connection.close()








def add_record_to_mysql(connection, table_name, record):
    """
    Agrega un registro a una tabla en MySQL.

    :param connection: Objeto de conexión a MySQL.
    :param table_name: Nombre de la tabla donde se insertará el registro.
    :param record: Diccionario con los datos del registro.
    """
    try:
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
        cursor.close()


def add_registro_mysql(mijsonreg):
    """
    Similar a add_registro para MongoDB, pero inserta un registro en MySQL.
    """
    table_name = "mitrack"  # Cambiar por el nombre de tu tabla
    connection = connect_to_mysql()

    if connection:
        try:
            add_record_to_mysql(connection, table_name, mijsonreg)
        finally:
            # Cerrar la conexión
            connection.close()



