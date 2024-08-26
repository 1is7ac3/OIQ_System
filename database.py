"""Import modules"""
import csv
import mysql.connector as maria
import data


def create_database():
    """funcion crear database inventory"""
    connection = maria.connect(**data.db_config_init)
    try:
        cursor = connection.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS inventory""")
    except maria.Error as err:
        print(err)
    cursor.close()
    connection.close()


def run_query(query, parameters=()):
    """funcion correr busqueda"""
    conn = None
    cursor = None
    try:
        conn = maria.Connect(**data.db_config)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        conn.commit()
        return result
    except maria.Error as err:
        print(f"Error: {err}")
        print(f"Consulta fallida: {cursor.statement}")
    finally:
        if cursor:
            conn.close()
        if conn:
            cursor.close()


def run_query_edit(query, parameters=()):
    """funcion correr edit"""
    conn = None
    cursor = None
    try:
        conn = maria.Connect(**data.db_config)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()
        return 1
    except maria.Error as err:
        print(f"Error: {err}")
        print(f"Cambio fallido: {cursor.statement}")
        if err.errno == maria.errorcode.ER_DUP_ENTRY:
            return 2
    finally:
        if cursor:
            conn.close()
        if conn:
            cursor.close()


def create_table():
    """funcion crear tablas"""
    connection = maria.Connect(**data.db_config)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS product (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        code VARCHAR(255) UNIQUE, name VARCHAR(255),
                        price_buy INT, ganancia INT, price_sales INT,
                        location INT, location2 INT, location3 INT) """)
        connection.commit()

    except maria.errors.IntegrityError as err:
        print(err)
    cursor.close()
    connection.close()


def create_table_sales():
    """funcion crear tablas"""
    connection = maria.Connect(**data.db_config)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS sales (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) UNIQUE, quantity INT, price INT) """
        )
        connection.commit()

    except maria.errors.IntegrityError as err:
        print(err)
    cursor.close()
    connection.close()


def create_database_users():
    """funcion crear table users"""
    connection = maria.Connect(**data.db_config)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
           id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE,
           password VARCHAR(255))"""
        )
        connection.commit()

    except maria.errors.IntegrityError as err:
        print(err)
    cursor.close()
    connection.close()


def create_database_history():
    """funcion crear table history"""
    connection = maria.Connect(**data.db_config)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS history(
            id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price INT,
            quantity INT, user VARCHAR(255), action VARCHAR(255), date VARCHAR(255))"""
        )
        connection.commit()

    except maria.errors.IntegrityError as err:
        print(err)
    cursor.close()
    connection.close()


def csv_import(file_name):
    """Función import cvs"""
    with open(file_name, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        f = 1
        for row in reader:
            query = """INSERT INTO product (code, name, price_buy, ganancia,
            price_sales, location, location2, location3)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            price = round(float(row[2]) * (1 + (float(row[3]) / 100)))
            parameters = (str(row[0].upper()), str(row[1].upper()),
                          round(float(row[2])), round(float(row[3])),
                          price, round(float(row[4])), round(float(row[5])),
                          round(float(row[6])))
            result = run_query_edit(query, parameters)
            print(result, maria.errorcode.ER_DUP_ENTRY)
            if result == 2:
                query_db_exist = """select price_buy, ganancia,
                    location, location2, location3, code from product"""
                db_rows = run_query(query_db_exist)
                for i in db_rows:
                    if i[5] == row[0]:
                        query = """UPDATE product SET price_buy=%s,
                        ganancia=%s, price_sales=%s, location=%s,
                        location2=%s, location3=%s WHERE code=%s"""
                        price_2 = round(float(row[2]) * (1 + (float(
                            row[3]) / 100)))
                        parameters = (row[2], row[3], price_2,
                                      round(int(row[4])+int(i[2])),
                                      round(int(row[5])+int(i[3])),
                                      round(int(row[6])+int(i[4])), i[5])
                        run_query_edit(query, parameters)
            f += 1
    csv_file.close()


def csv_export(file_name):
    """Función export cvs"""
    with open(file_name, "w", encoding="utf-8") as csv_file:
        write = csv.writer(csv_file, delimiter=";")
        query = """select code, name, price_buy, ganancia, location, location2,
        location3 from product order by name desc"""
        db_rows = run_query(query)
        for x in db_rows:
            write.writerow(x)
    csv_file.close()


def change():
    "Change datebase"
    query = """DROP table product"""
    run_query_edit(query)
