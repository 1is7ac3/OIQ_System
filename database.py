import sqlite3


def create_database():
    connection = sqlite3.connect("data.db")
    try:
        connection.execute("""CREATE TABLE "product"(
           'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
           'name' TEXT NOT NULL,
           'price' REAL NOT NULL,
           'quantity' REAL NOT NULL,
           'code' REAL NOT NULL
        )""")

        cursor = connection.execute("select id, name, price from product")
        for fila in cursor:
            print(fila)
        connection.close()
        print("Se creo la tabla de articulos")
    except sqlite3.OperationalError:
        print("La tabla de articulos ya existe")
    connection.close()


def create_database_customers():
    connection = sqlite3.connect("customers.db")
    try:
        connection.execute("""CREATE TABLE "agenda_customers"(
           'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
           'name' TEXT NOT NULL,
           'phone' REAL NOT NULL,
           'order' REAL NOT NULL,
           'order_date' REAL NOT NULL,
           'delivery_date' REAL NOT NULL,
           'advance' REAL NOT NULL
        )""")

        cursor = connection.execute("select id, name, price, date, shopping from sales")
        for fila in cursor:
            print(fila)
        connection.close()
        print("Se creo la tabla de articulos")
    except sqlite3.OperationalError:
        print("La tabla de articulos ya existe")
    connection.close()


def create_database_sales():
    connection = sqlite3.connect("sales.db")
    try:
        connection.execute("""CREATE TABLE "sales"(
           'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
           'name' TEXT NOT NULL,
           'price' REAL NOT NULL
        )""")

        cursor=connection.execute("select id, name, price from sales")
        for fila in cursor:
            print(fila)
        connection.close()
        print("Se creo la tabla de articulos")
    except sqlite3.OperationalError:
        print("La tabla de articulos ya existe")
    connection.close()


def create_database_history():
    connection = sqlite3.connect("history.db")
    try:
        connection.execute("""CREATE TABLE "history"(
           'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
           'name' TEXT NOT NULL,
           'price' REAL NOT NULL,
           'date' REAL NOT NULL,
           'sale' REAL NOT NULL
        )""")

        cursor = connection.execute("select id, name, price, date, shopping from sales")
        for fila in cursor:
            print(fila)
        connection.close()
        print("Se creo la tabla de articulos")
    except sqlite3.OperationalError:
        print("La tabla de articulos ya existe")
    connection.close()


def create_database_users():
    connection = sqlite3.connect("users.db")
    try:
        connection.execute("""CREATE TABLE "users"(
           'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
           'user' TEXT NOT NULL,
           'password' REAL NOT NULL
        )""")

        cursor = connection.execute("select id, name, price from product")
        for fila in cursor:
            print(fila)
        connection.close()
        print("Se creo la tabla de articulos")
    except sqlite3.OperationalError:
        print("La tabla de articulos ya existe")
    connection.close()