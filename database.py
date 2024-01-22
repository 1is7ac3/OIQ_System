'''Import modules'''
import csv
import mysql.connector as maria
import data


def create_database_mariadb():
    '''funcion crear database inventory'''
    connection = maria.connect(**data.db_config_init)
    try:
        cursor = connection.cursor()
        cursor.execute('''CREATE DATABASE IF NOT EXISTS inventory''')
        print('Se creo la base de datos inventory')
    except maria.Error as err:
        print(err)
    cursor.close()
    connection.close()


def run_query_mariadb(query, parameters=()):
    '''funcion correr busqueda'''
    conn = None
    cursor = None
    try:
        conn = maria.connect(**data.db_config)
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


def run_query_mariadb_edit(query, parameters=()):
    '''funcion correr edit'''
    conn = None
    cursor = None
    try:
        conn = maria.connect(**data.db_config)
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


def create_table_mariadb():
    '''funcion crear tablas'''
    connection = maria.connect(**data.db_config)
    try:
        cursor = connection.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS product (
                        id INT AUTO_INCREMENT PRIMARY KEY, code VARCHAR(255),
                        name VARCHAR(255) UNIQUE, quantity INT, price_buy INT,
                        ganancia INT, price_sales INT, location VARCHAR(255)
                        ) ''')
        connection.commit()
        print('Se creo la tabla product')
    except maria.errors.IntegrityError as err:
        print(err)
    cursor.close()
    connection.close()


def create_table_sales_mariadb():
    '''funcion crear tablas'''
    connection = maria.connect(**data.db_config)
    try:
        cursor = connection.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS sales (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) UNIQUE, quantity INT, price INT) ''')
        connection.commit()
        print('Se creo la tabla de sales')
    except maria.errors.IntegrityError as err:
        print(err)
    cursor.close()
    connection.close()


def create_database_users():
    '''funcion crear table users'''
    connection = maria.connect(**data.db_config)
    try:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
           id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE,
           password VARCHAR(255))''')
        connection.commit()
        print('Se creo la tabla users')
    except maria.errors.IntegrityError as err:
        print(err)
    cursor.close()
    connection.close()


def create_database_history():
    '''funcion crear table users'''
    connection = maria.connect(**data.db_config)
    try:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS history(
            id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price INT,
            sale VARCHAR(255), date VARCHAR(255))''')
        connection.commit()
        print('Se creo la tabla users')
    except maria.errors.IntegrityError as err:
        print(err)
    cursor.close()
    connection.close()


def csv_import(file_name):
    '''Funcion import cvs'''
    with open(file_name, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            query = '''INSERT INTO product (code, name, quantity,
            price_buy, ganancia, price_sales, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            price = round(float(row[3]) * (1 + (float(row[4]) / 100)))
            parameters = (str(row[0].upper()), str(row[1].upper()),
                          round(float(row[2])), round(float(row[3])),
                          round(float(row[4])), price, str(row[5].upper()))
            result = run_query_mariadb_edit(query, parameters)
            print(result, maria.errorcode.ER_DUP_ENTRY)
            if result == 2:
                query_db_exist = '''select quantity, price_buy, ganancia,
                    location, name from product'''
                db_rows = run_query_mariadb(query_db_exist)
                for i in db_rows:
                    if i[4] == row[1]:
                        cantidad = i[0]
                query = '''UPDATE product SET quantity=%s, price_buy=%s,
                ganancia=%s, price_sales=%s, location=%s WHERE name=%s'''
                price_2 = round(float(row[3]) * (1 + (float(row[4]) / 100)))
                new_c = int(row[2]) + int(cantidad)
                parameters = (new_c, row[3], row[4], price_2,
                              str(row[5].upper()), row[1])
                run_query_mariadb_edit(query, parameters)
    csv_file.close()
