'''Import modules'''
import csv
import mysql.connector as maria

db_config = {'host': '127.0.0.1', 'user': 'root', 'password': '7983449',
             'database': 'inventory'}
db_config_init = {'host': '127.0.0.1', 'user': 'root', 'password': '7983449'}


def create_database_mariadb():
    '''funcion crear database inventory'''
    connection = maria.connect(**db_config_init)
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
        conn = maria.connect(**db_config)
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
        conn = maria.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()
    except maria.Error as err:
        print(f"Error: {err}")
        print(f"Cambio fallido: {cursor.statement}")
    finally:
        if cursor:
            conn.close()
        if conn:
            cursor.close()


def create_table_mariadb():
    '''funcion crear tablas'''
    connection = maria.connect(**db_config)
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
    connection = maria.connect(**db_config)
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
    connection = maria.connect(**db_config)
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
    connection = maria.connect(**db_config)
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
            try:
                query = '''INSERT INTO product (code, name, quantity,
                price_buy, ganancia, price_sales, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                price = round(float(row[3]) * (1 + (float(row[4]) / 100)))
                parameters = (row[0], row[1], round(float(row[2])), round(
                    float(row[3])), round(float(row[4])), price, row[5])
                run_query_mariadb_edit(query, parameters)
            except maria.errors.IntegrityError as err:
                if err == maria.errorcode.ER_DUP_ENTRY:
                    query_db_exist = '''select quantity, price_buy, ganancia,
                    location from product'''
                    db_rows = run_query_mariadb(query_db_exist)
                    for i in db_rows:
                        query = '''UPDATE product SET quantity=%s,
                         price_buy=%s, ganancia=%s, price_sales=%s, location=%s
                         WHERE quantity=%s AND price_buy=%s AND ganancia=%s
                         AND location=%s'''
                        price_2 = round(float(row[3]) * (1 + (float(
                            row[4]) / 100)))
                        new_c = round(row[2] + i[0])
                        parameters = (
                            new_c, row[3], row[4], price_2, row[5], i[0], i[1],
                            i[2], i[3])
                        run_query_mariadb_edit(query, parameters)
    csv_file.close()
