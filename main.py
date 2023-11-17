from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import sqlite3
import datetime
import os
import shutil
import database

PASSWORD_ROOT = '1234'


class Product:
    db_name = 'data.db'
    db_sales = 'sales.db'
    db_history = 'history.db'
    db_customers = 'customers.db'
    db_users = 'users.db'

    def __init__(self, window, user, money):
        self.wind = window
        self.wind.title('Inventario')
        self.total = tk.DoubleVar(value=0)
        self.deposito = tk.DoubleVar(value=0)
        self.cambio = tk.DoubleVar(value=0)
        self.calculadora = tk.DoubleVar(value=0)
        self.user = tk.StringVar(value=user)
        self.password = tk.StringVar()
        self.total_caja = tk.DoubleVar(value=0)
        tm = datetime.datetime.now()
        self.DiaInicio = tk.IntVar(value=tm.day)
        self.HoraInicio = tk.IntVar(value=tm.hour)
        self.MinutoInicio = tk.IntVar(value=tm.minute)
        menubar = tk.Menu(self.wind)
        self.wind.config(menu=menubar)
        file_corte = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Usuario', menu=file_corte)
        file_corte.add_command(label='cierre de caja', command=lambda: self.historial_ventas(money, user))
        file_corte.add_separator()
        file_corte.add_command(label='Agregar usuario', command=self.add_user)
        file_corte.add_command(label='Eliminar usuario')
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Archivo', menu=file_menu)
        file_menu.add_command(label='Abrir un historial', command=self.table_history_old)
        file_menu.add_separator()
        file_menu.add_command(label='Cerrar sesión', command=self.wind.quit)
        file_customers = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Clientes', menu=file_customers)
        file_customers.add_command(label='Historial de clientes', command=self.ventana_clientes)
        frame = tk.LabelFrame(self.wind, text='Inventario Productos')
        frame.place(x=0, y=0, width=500, height=110)
        frame.grid(row=3, column=5)
        tk.Label(frame, text='Nombre: ').grid(row=0, column=0)
        self.name = tk.Entry(frame)
        self.name.focus()
        self.name.grid(row=0, column=1)
        tk.Label(frame, text='Precio: ').grid(row=0, column=2)
        self.price = tk.Entry(frame)
        self.price.grid(row=0, column=3)
        tk.Label(frame, text='Cantidad: ').grid(row=1, column=0)
        self.cantidad = tk.Entry(frame)
        self.cantidad.grid(row=1, column=1)
        tk.Label(frame, text='Código: ').grid(row=1, column=2)
        self.code = tk.Entry(frame)
        self.code.grid(row=1, column=3)
        ttk.Button(frame, text='Guardar producto', command=self.add_product).grid(row=3, column=0)
        self.message = tk.Label(text='', fg='white', bg='#00AAE4')
        self.message.place(x=0, y=110, width=781, height=30)
        self.tree = ttk.Treeview(self.wind, columns=('name', 'price', 'code'))
        self.tree.place(x=0, y=138, width=800, height=500)
        self.tree.column('#0', width=350)
        self.tree.heading('#0', text='NOMBRE', anchor=tk.CENTER)
        self.tree.column('#1', width=100, anchor=tk.CENTER)
        self.tree.heading('#1', text='PRECIO', anchor=tk.CENTER)
        self.tree.column('#2', width=30, anchor=tk.CENTER)
        self.tree.heading('#2', text='CANTIDAD', anchor=tk.CENTER)
        self.tree.column('#3', width=100)
        self.tree.heading('#3', text='CÓDIGO', anchor=tk.CENTER)
        self.scrollbarO = ttk.Scrollbar(self.wind, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbarO.place(x=780, y=138, width=30, height=500)
        self.tree.configure(yscrollcommand=self.scrollbarO.set)
        ttk.Button(text='Eliminar',
                   command=lambda: self.confirm_authorization(1)).place(x=0, y=638, width=180, height=30)
        ttk.Button(text='Editar',
                   command=lambda: self.confirm_authorization(2)).place(x=180, y=638, width=180, height=30)
        ttk.Button(text='Devoluciones',
                   command=lambda: self.rembolso(self.tree.selection())).place(x=360, y=638, width=200, height=30)
        self.entry_search_var = tk.StringVar()
        self.entry_search = tk.Entry(self.wind, textvariable=self.entry_search_var)
        self.entry_search.place(x=560, y=638, width=200, height=30)
        self.entry_search_var.trace('w', self.search)
        self.update_table()
        frame_shopping = tk.LabelFrame(self.wind, text='Registra un nuevo producto')
        frame_shopping.place(x=805, y=0, width=600, height=440)
        self.troo = ttk.Treeview(self.wind, columns='product')
        self.troo.place(x=820, y=30, width=500, height=300)
        self.troo.heading('#0',  text='Producto', anchor=tk.CENTER)
        self.troo.column('#1', anchor=tk.CENTER, width=50)
        self.troo.heading('#1', text='Precio', anchor=tk.CENTER)
        self.scrollbar = ttk.Scrollbar(self.wind, orient=tk.VERTICAL, command=self.troo.yview)
        self.scrollbar.place(x=1320, y=30, width=30, height=300)
        self.troo.configure(yscrollcommand=self.scrollbar.set)
        self.messageVentas = tk.Label(frame_shopping, fg='black', bg='red')
        self.messageVentas.place(x=840, y=300, width=400, height=30)
        ttk.Button(text='Cobrar', command=self.cobrar).place(x=820, y=330, width=200, height=30)
        ttk.Button(text='Eliminar producto', command=self.eliminarCompra).place(x=1000, y=330, width=200, height=30)
        ttk.Button(text='+', command=lambda: self.agregarProducto(self.tree.selection())).place(
            x=1188, y=330, width=50, height=30)
        self.update_table_sales()
        tk.Label(self.wind, text='TOTAL: ', fg='blue').place(x=820, y=385, width=94, height=30)
        tk.Label(self.wind, text='$', fg='blue').place(x=900, y=378, width=20, height=40)
        tk.Entry(self.wind, textvariable=self.total, state='readonly', fg='blue').place(
            x=920, y=380, width=200, height=40)
        ttk.Button(text='Ventas del dia y devoluciones', command=lambda: self.historial_ventas(money, user)).place(
            x=1000, y=640, width=300, height=30)

    def search(self, *args):
        item_tree = self.tree.get_children()
        search = self.entry_search_var.get().upper()
        for item in item_tree:
            if search == '':
                self.update_table()
            if search in self.tree.item(item)['text']:
                search_var = self.tree.item(item)
                self.tree.delete(item)
                if float(search_var['values'][1]) < 1:
                    self.tree.insert('', 0,
                                     text=search_var['text'], values=(search_var['values'][0], search_var['values'][1],
                                                                      search_var['values'][2]), tags='bg_red')
                    self.tree.tag_configure('bg_red', background='red')
                elif float(search_var['values'][1]) > 1:
                    self.tree.insert('', 0,
                                     text=search_var['text'], values=(search_var['values'][0], search_var['values'][1],
                                                                      search_var['values'][2]), tags='bg_green')
                    self.tree.tag_configure('bg_green', background='green')
                else:
                    self.tree.insert('', 0,
                                     text=search_var['text'], values=(search_var['values'][0], search_var['values'][1],
                                                                      search_var['values'][2]), tags='bg_yellow')
                    self.tree.tag_configure('bg_yellow', background='yellow')

    def rgb(self, a, b, c):
        return '#%02x%02x%02x' % (a, b, c)

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def update_table(self):
        self.destroy_window()
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'select id, name, price, quantity, code from product order by name desc'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[3] < 1:
                self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[4]), tags='bg_red')
                self.tree.tag_configure('bg_red', background='red')
            elif row[3] > 1:
                self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[4]), tags='bg_green')
                self.tree.tag_configure('bg_green', background='#48E120')
            else:
                self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[4]), tags='bg_yellow')
                self.tree.tag_configure('bg_yellow', background='yellow')

    def validation(self):
        if len(self.name.get()) != 0 and len(self.price.get()) != 0:
            return True
        else:
            return False

    def validation_duplicate(self):
        if self.price.get().isdigit() and self.cantidad.get().isdigit():
            return 1
        else:
            return 2

    def add_product(self):
        self.destroy_window()
        if self.validation():
            option = self.validation_duplicate()
            if option == 1:
                query = 'insert into product (name, price, quantity, code) values (?, ?, ?, ?)'
                parameters = (self.name.get().upper(), self.price.get(), self.cantidad.get(), self.code.get())
                self.run_query(query, parameters)
                self.message['text'] = 'Producto {} fue agregado'.format(self.name.get())
                self.name.delete(0, tk.END)
                self.price.delete(0, tk.END)
                self.cantidad.delete(0, tk.END)
                self.code.delete(0, tk.END)
                self.update_table()
            if option == 2:
                self.message['text'] = 'Verificar que los datos sean correctos'
        else:
            self.message['text'] = 'El nombre y el precio son requeridos.'

    def delete_product(self, id_data):
        self.destroy_window()
        self.message['text'] = ''
        try:
            self.tree.item(id_data)['text'][0]
        except IndexError as e:
            self.message['text'] = 'por favor seleccione un producto'
            return
        self.message['text'] = ''
        name = self.tree.item(id_data)['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'El dato {} fue eliminado correctamente'.format(name)
        self.update_table()

    def confirm_authorization(self, option):
        self.destroy_window()
        self.authorization_wind = tk.Toplevel()
        self.authorization_wind.title = 'Autorización'
        self.authorization_wind.geometry('500x210')
        self.authorization_wind.resizable(False, False)
        tk.Label(self.authorization_wind, text='contraseña principal').pack()
        clave = tk.Entry(self.authorization_wind,
                         textvariable=tk.StringVar(self.authorization_wind, value=''), show='*')
        clave.pack()
        tk.Button(self.authorization_wind, text='Ingresar', command=lambda: self.verify_key(clave.get(), option)).pack()

    def verify_key(self, password, option):
        self.authorization_wind.destroy()
        if password == PASSWORD_ROOT:
            if option == 1:
                self.delete_product(self.tree.selection())
            else:
                self.edit_product(self.tree.selection())
        else:
            messagebox.showwarning('Error', 'Contraseña incorrecta')
            self.authorization_wind.destroy()

    def edit_product(self, id_data):
        self.destroy_window()
        self.message['text'] = ''

        try:
            self.tree.item(id_data)['text'][0]
        except IndexError as e:
            self.message['text'] = 'por favor seleccione un producto'
            return

        name = self.tree.item(id_data)['text']
        old_price = self.tree.item(id_data)['values'][0]
        old_quantity = self.tree.item(id_data)['values'][1]
        old_code = self.tree.item(id_data)['values'][2]

        self.edit_wind = tk.Toplevel()
        self.edit_wind.title = 'Editar producto'
        self.edit_wind.geometry('320x320')
        self.edit_wind.resizable(False, False)

        tk.Label(self.edit_wind, text='Antiguo nombre').grid(row=0, column=1)
        tk.Entry(self.edit_wind,
                 textvariable=tk.StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

        tk.Label(self.edit_wind, text='Nuevo nombre').grid(row=1, column=1)
        new_name = tk.Entry(self.edit_wind, textvariable=tk.StringVar(self.edit_wind, value=name))
        new_name.grid(row=1, column=2)

        tk.Label(self.edit_wind, text='Antiguo precio').grid(row=2, column=1)
        tk.Entry(self.edit_wind,
                 textvariable=tk.StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)

        tk.Label(self.edit_wind, text='Nuevo precio').grid(row=3, column=1)
        new_price = tk.Entry(self.edit_wind, textvariable=tk.StringVar(self.edit_wind, value=old_price))
        new_price.grid(row=3, column=2)

        # old cantidad
        tk.Label(self.edit_wind, text='Antigua cantidad').grid(row=4, column=1)
        tk.Entry(self.edit_wind,
                 textvariable=tk.StringVar(self.edit_wind, value=old_quantity), state='readonly').grid(row=4, column=2)
        # Cantidad
        tk.Label(self.edit_wind, text='Nueva cantidad').grid(row=5, column=1)
        new_cantidad = tk.Entry(self.edit_wind, textvariable=tk.StringVar(self.edit_wind, value=old_quantity))
        new_cantidad.grid(row=5, column=2)

        tk.Label(self.edit_wind, text='código Antiguo').grid(row=6, column=1)
        tk.Entry(self.edit_wind,
                 textvariable=tk.StringVar(self.edit_wind, value=old_code), state='readonly').grid(row=6, column=2)
        tk.Label(self.edit_wind, text='Nuevo código').grid(row=7, column=1)
        self.new_code = tk.Entry(self.edit_wind, textvariable=tk.StringVar(self.edit_wind, value=old_code))
        self.new_code.grid(row=7, column=2)
        tk.Button(self.edit_wind, text='Guardar',
                  command=lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price,
                                                    new_cantidad.get(), old_quantity, self.new_code.get(), old_code
                                                    )).grid(row=8, column=2, sticky=tk.W + tk.E)

    def edit_records(self, new_name, name, new_price, old_price, new_cantidad, old_quantity, new_code, old_code):

        self.destroy_window()
        query = ('UPDATE product SET name=?, price=?, quantity=?, code=? WHERE name=? AND price=?'
                 ' AND quantity=? AND code=?')
        parameters = (new_name, new_price, new_cantidad, new_code, name, old_price, old_quantity, old_code)
        self.run_query(query, parameters)
        self.message['text'] = 'El dato {} fue actualizado'.format(name)
        self.update_table()

    def run_queryVentas(self, query, parameters=()):
        with sqlite3.connect(self.db_sales) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def update_table_sales(self):
        self.total.set(0)
        records = self.troo.get_children()
        for element in records:
            self.troo.delete(element)
        query = 'select id, name, price from sales'
        db_rows = self.run_queryVentas(query)
        for row in db_rows:
            self.troo.insert('', 0, text=row[1], values=(row[2], row[0]))
            self.total.set(self.total.get() + row[2])

    def agregarProducto(self, id_data):
        self.messageVentas['text'] = ''
        try:
            self.tree.item(id_data)['text']
        except IndexError:
            self.message['text'] = 'porfavor seleccione un producto'
            return
        cantidad = self.tree.item(id_data)['values'][1]
        cantidad = float(cantidad)
        if cantidad > 0:
            query = 'insert into sales (id, name, price) values (NULL, ?, ?)'
            name = self.tree.item(id_data)['text']
            price = self.tree.item(id_data)['values'][0]
            parameters = (name, price)
            self.run_queryVentas(query, parameters)
            self.messageVentas['text'] = 'Producto {} fue agregado'.format('gansito')
            # actualizar
            self.update_table_sales()
        elif cantidad <= 0:
            self.message['text'] = ''
            self.message['text'] = 'No hay suficiente producto'

    def eliminarCompra(self):
        self.messageVentas['text'] = ''
        try:
            self.troo.item(self.troo.selection())['text']
        except IndexError:
            self.messageVentas['text'] = 'por favor seleccione un producto'
            return
        self.messageVentas['text'] = ''
        name = self.troo.item(self.troo.selection())['values'][1]

        # eliminar el dato seleccionado
        query = 'DELETE FROM sales WHERE id = ?'
        self.run_queryVentas(query, (name,))
        self.messageVentas['text'] = 'El dato {} fue eliminado correctamente'.format(name)
        self.update_table_sales()

    # cobrar productos
    def cobrar(self):
        self.destroy_window()
        self.cobrar_wind = tk.Toplevel()
        self.cobrar_wind.title = 'Cobrar producto'
        self.cobrar_wind.geometry('320x200')
        self.cambio.set(value=0)
        tk.Label(self.cobrar_wind, text='TOTAL').grid(row=0, column=0)
        tk.Entry(self.cobrar_wind, textvariable=self.total, state='readonly').grid(row=0, column=1)
        tk.Label(self.cobrar_wind, text='Pago').grid(row=1, column=0)
        self.deposito = tk.Entry(self.cobrar_wind)
        self.deposito.grid(row=1, column=1)
        tk.Label(self.cobrar_wind, text='Cambio').grid(row=2, column=0)
        tk.Entry(self.cobrar_wind, textvariable=self.cambio, state='readonly').grid(row=2, column=1)

        tk.Button(self.cobrar_wind, text='cobrar', command=self.cambioVenta).grid(row=3, column=1, sticky=tk.W + tk.E)

    def cambioVenta(self):
        diferencia = float(self.deposito.get()) - self.total.get()
        if diferencia >= 0:

            self.cambio.set(diferencia)

            store_list = self.tree.get_children()
            for store_data in store_list:

                product_store = self.tree.item(store_data)['text']
                price = self.tree.item(store_data)['values'][0]
                quantity = self.tree.item(store_data)['values'][1]
                code_qr = self.tree.item(store_data)['values'][2]

                sales_list = self.troo.get_children()
                for sales_data in sales_list:

                    sales_product = self.troo.item(sales_data)['text']

                    if product_store == sales_product:

                        price = float(price)
                        quantity = float(quantity)
                        new_quantity = quantity - 1
                        code_qr = str(code_qr)

                        if new_quantity >= 0:
                            query = ('UPDATE product SET name=?, price=?, quantity=?, code=? WHERE name=? AND price=? '
                                     'AND quantity=? AND code=?')
                            parameters = (product_store, price, new_quantity, code_qr, product_store, price, quantity,
                                          code_qr)
                            self.run_query(query, parameters)

                            quantity = new_quantity

                            self.add_product_history(product_store, price, 'Compra')

            self.update_table()
            # eliminar datos
            listVenta2 = self.troo.get_children()
            for datoVenta2 in listVenta2:
                # name=self.troo.item(datoVenta2)['text']
                id = self.troo.item(datoVenta2)['values'][1]
                # eliminar el dato seleccionado
                query = 'DELETE FROM sales WHERE id = ?'
                self.run_queryVentas(query, (id,))
            self.update_table_sales()

        else:
            messagebox.showwarning('Error', 'Deposite mas dinero')

    def run_query_history(self, query, parameters=()):
        with sqlite3.connect(self.db_history) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def add_product_history(self, name, price, sale):

        query = 'insert into history (id, name, price, date, sale) values (NULL, ?, ?, ?, ?)'

        date = datetime.datetime.now()
        parameters = (name, price, date, sale)
        self.run_query_history(query, parameters)

    def rembolso(self, id_data):
        self.destroy_window()
        self.message['text'] = ''
        try:
            self.tree.item(id_data)['text'][0]
        except IndexError as e:
            self.message['text'] = 'por favor seleccione un producto'
            return
        self.edit_rembolso = tk.Toplevel()
        self.edit_rembolso.title = 'Editar historial'
        self.edit_rembolso.geometry('320x200')
        name = self.tree.item(id_data)['text']
        price = self.tree.item(id_data)['values'][0]
        cantidad = self.tree.item(id_data)['values'][1]
        code = self.tree.item(id_data)['values'][2]
        tk.Label(self.edit_rembolso, text='Antiguo nombre').grid(row=0, column=1)
        tk.Entry(self.edit_rembolso,
                 textvariable=tk.StringVar(self.edit_rembolso, value=name), state='readonly').grid(row=0, column=2)

        tk.Label(self.edit_rembolso, text='Antiguo precio').grid(row=1, column=1)
        tk.Entry(self.edit_rembolso, textvariable=tk.StringVar(
            self.edit_rembolso, value=price), state='readonly').grid(row=1, column=2)

        tk.Label(self.edit_rembolso, text='Antigua cantidad').grid(row=2, column=1)
        tk.Entry(self.edit_rembolso,
                 textvariable=tk.StringVar(self.edit_rembolso, value=cantidad), state='readonly').grid(row=2, column=2)
        new_cantidad = float(cantidad) + 1
        tk.Button(self.edit_rembolso, text='Rembolsar',
               command=lambda: self.rembolso_actualizar(name, price, new_cantidad, cantidad, code)).grid(
            row=4, column=2, sticky=tk.W + tk.E)

    def rembolso_actualizar(self, name, price, new_cantidad, cantidad, code):
        self.edit_records(name, name,
                          price, price, new_cantidad, cantidad, code, code)
        self.add_product_history(name, price, 'reembolso')

    def actualizarHistorial(self, dinero):
        records = self.tree_historial.get_children()
        for element in records:
            self.tree_historial.delete(element)
        query = 'select id, name, price, date, sale from history'
        db_rows = self.run_query_history(query)
        dinero = float(dinero)
        self.total_caja.set(dinero)
        date = datetime.datetime.now()

        for row in db_rows:
            self.tree_historial.insert('', 0, text=row[1], values=(row[2], row[4], row[3]))
            # comprobar si es una compra o un rembolso para sumar print(self.HoraInicio.get())
            # self.DiaInicio=StringVar(value=tm.day)
            # self.HoraInicio=StringVar(value=tm.hour)
            # self.MinutoInicio=StringVar(value=tm.minute)
            if str(row[4]) == 'Compra':
                self.total_caja.set(self.total_caja.get() + row[2])
    def historial_ventas(self, dinero, usuario):
        self.wind_historial = tk.Toplevel()
        self.wind_historial.geometry('1100x400')
        self.wind_historial.resizable(False, False)
        self.wind_historial.title('Historial de ventas')
        self.tree_historial = ttk.Treeview(self.wind_historial, height=2, columns=('name', 'price', ''))
        self.tree_historial.place(x=20, y=10, width=1030, height=300)
        self.tree_historial.heading('#0', text='Producto', anchor=tk.CENTER)
        self.tree_historial.heading('#1', text='Precio', anchor=tk.CENTER)
        self.tree_historial.heading('#2', text='devolución o compra', anchor=tk.CENTER)
        self.tree_historial.heading('#3', text='date', anchor=tk.CENTER)
        scrollbarO_historial = ttk.Scrollbar(self.wind_historial, orient=tk.VERTICAL, command=self.tree_historial.yview)
        scrollbarO_historial.place(x=1050, y=10, width=20, height=300)
        self.tree_historial.configure(yscrollcommand=scrollbarO_historial.set)
        self.actualizarHistorial(dinero)
        tk.Label(self.wind_historial, text='TOTAL', fg='blue').place(x=20, y=340, width=94, height=30)
        tk.Entry(self.wind_historial, textvariable=self.total_caja, state='readonly', fg='blue').place(
            x=114, y=340, width=94, height=30)
        ttk.Button(self.wind_historial, text='Corte',
                   command=lambda: self.corteCaja(usuario, self.total_caja, dinero)).place(x=930, y=360, width=94,
                                                                                           height=30)

    def borrar_historial(self, money):
        records = self.tree_historial.get_children()
        for element in records:
            name = self.tree_historial.item(element)['text']
            print(name)
            query = 'DELETE FROM history WHERE name = ?'
            self.run_query_history(query, (name,))
        self.actualizarHistorial(money)

    def run_query_customers(self, query, parameters=()):
        with sqlite3.connect(self.db_customers) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def ventana_clientes_actualizar(self):
        records = self.tree_clientes.get_children()
        for element in records:
            self.tree_clientes.delete(element)
        query = 'select id, name, celular, pedido, date_pedido, date_entrega, anticipo from customers'
        db_rows = self.run_query_customers(query)
        for row in db_rows:
            self.tree_clientes.insert(
                '', 0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6]), tags='bg')

    def guardar_cliente(self, name, phone, order, order_date, delivery_date, advance):

        self.nameCliente.delete(0, tk.END)
        self.celularCliente.delete(0, tk.END)
        self.pedidoCliente.delete(0, tk.END)
        self.date_pedidoCliente.delete(0, tk.END)
        self.date_entregaCliente.delete(0, tk.END)
        self.anticipoCliente.delete(0, tk.END)
        query = 'insert into agenda_customers (id, name, phone, order, order_date, delivery_date, advance)' \
                'values (NULL, ?, ?, ?, ?, ?, ?)'
        parameters = (name, phone, order, order_date, delivery_date, advance)
        self.run_query_customers(query, parameters)
        self.ventana_clientes_actualizar()

    def eliminar_clientes(self):
        try:
            self.tree_clientes.item(self.tree_clientes.selection())['text']
        except IndexError as e:
            return messagebox.showwarning('Error', 'Elige a un cliente')

        self.message['text'] = ''
        name = self.tree_clientes.item(self.tree_clientes.selection())['text']
        query = 'DELETE FROM customers WHERE name = ?'
        self.run_query_customers(query, (name,))

        self.ventana_clientes_actualizar()

    def ventana_clientes(self):
        ventana_clientes = tk.Toplevel()
        ventana_clientes.geometry('540x400')
        ventana_clientes.resizable(False, False)
        ventana_clientes.title('ventana de clientes')

        frame = tk.LabelFrame(ventana_clientes, text='Añadir Clientes')
        frame.place(x=0, y=0, width=500, height=150)

        tk.Label(frame, text='Nombre: ').place(x=60, y=2, width=60, height=10)
        self.nameCliente = tk.Entry(frame, textvariable=tk.StringVar(ventana_clientes))
        self.nameCliente.place(x=120, y=0, width=120, height=20)
        self.nameCliente.focus()

        tk.Label(frame, text='Celular: ').place(x=60, y=32, width=60, height=10)
        self.celularCliente = tk.Entry(frame, textvariable=tk.StringVar(ventana_clientes))
        self.celularCliente.place(x=120, y=30, width=120, height=20)

        tk.Label(frame, text='Pedido: ').place(x=60, y=62, width=60, height=10)
        self.pedidoCliente = tk.Entry(frame, textvariable=tk.StringVar(ventana_clientes))
        self.pedidoCliente.place(x=120, y=60, width=120, height=20)

        tk.Label(frame, text='date pedido: ').place(x=250, y=2, width=100, height=10)
        self.date_pedidoCliente = tk.Entry(frame, textvariable=tk.StringVar(ventana_clientes))
        self.date_pedidoCliente.place(x=340, y=0, width=120, height=20)

        tk.Label(frame, text='date entrega: ').place(x=250, y=32, width=100, height=10)
        self.date_entregaCliente = tk.Entry(frame, textvariable=tk.StringVar(ventana_clientes))
        self.date_entregaCliente.place(x=340, y=30, width=120, height=20)

        tk.Label(frame, text='Anticipo: ').place(x=250, y=62, width=100, height=10)
        self.anticipoCliente = tk.Entry(frame, textvariable=tk.StringVar(ventana_clientes))
        self.anticipoCliente.place(x=340, y=60, width=120, height=20)

        ttk.Button(
            frame, text='Guardar', command=lambda:
            self.guardar_cliente(self.nameCliente.get(), self.celularCliente.get(), self.pedidoCliente.get(),
                                 self.date_pedidoCliente.get(), self.date_entregaCliente.get(),
                                 self.anticipoCliente.get())).place(x=165, width=210, height=30)
        self.tree_clientes = ttk.Treeview(ventana_clientes, height=6, columns='name')
        self.tree_clientes.place(x=0, y=160, width=500, height=200)
        # encabezado de tabla
        self.tree_clientes.heading('#0', text='Nombre', anchor=tk.CENTER)
        self.tree_clientes.heading('#1', text='celular', anchor=tk.CENTER)

        self.scrollbarO = ttk.Scrollbar(ventana_clientes, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.scrollbarO.place(x=505, y=160, width=30, height=200)
        self.tree_clientes.configure(yscrollcommand=self.scrollbarO.set)
        self.ventana_clientes_actualizar()

        ttk.Button(ventana_clientes,
                   text='Revisar', command=self.ventana_clientes_editar).place(x=10, y=360, width=240, height=30)
        ttk.Button(ventana_clientes,
                   text='Eliminar', command=self.eliminar_clientes).place(x=250, y=360, width=250, height=30)

    def ventana_clientes_editar(self):
        try:
            self.tree_clientes.item(self.tree_clientes.selection())['text']


        except IndexError as e:
            return messagebox.showwarning('Error', 'Elige a un cliente')
        # obtener los datos del cliente
        name = self.tree_clientes.item(self.tree_clientes.selection())['text']
        celular = self.tree_clientes.item(self.tree_clientes.selection())['values'][0]
        pedido = self.tree_clientes.item(self.tree_clientes.selection())['values'][1]
        date_pedido = self.tree_clientes.item(self.tree_clientes.selection())['values'][2]
        date_entrega = self.tree_clientes.item(self.tree_clientes.selection())['values'][3]
        anticipo = self.tree_clientes.item(self.tree_clientes.selection())['values'][4]
        self.ventana_clientes_edit = tk.Toplevel()
        self.ventana_clientes_edit.geometry('500x150')
        self.ventana_clientes_edit.resizable(False, False)
        self.ventana_clientes_edit.title('Revision de clientes')
        frame = tk.LabelFrame(self.ventana_clientes_edit, text='Revision Clientes')
        frame.place(x=0, y=0, width=500, height=150)
        tk.Label(frame, text='Nombre: ').place(x=60, y=2, width=60, height=10)
        new_name = tk.Entry(frame, textvariable=tk.StringVar(self.ventana_clientes_edit, value=name))
        new_name.place(x=120, y=0, width=120, height=20)
        tk.Label(frame, text='Celular: ').place(x=60, y=32, width=60, height=10)
        new_celular = tk.Entry(frame, textvariable=tk.StringVar(self.ventana_clientes_edit, value=celular))
        new_celular.place(x=120, y=30, width=120, height=20)
        tk.Label(frame, text='Pedido: ').place(x=60, y=62, width=60, height=10)
        new_pedido = tk.Entry(frame, textvariable=tk.StringVar(self.ventana_clientes_edit, value=pedido))
        new_pedido.place(x=120, y=60, width=120, height=20)
        tk.Label(frame, text='date pedido: ').place(x=250, y=2, width=100, height=10)
        new_date_pedido = tk.Entry(frame, textvariable=tk.StringVar(self.ventana_clientes_edit, value=date_pedido))
        new_date_pedido.place(x=340, y=0, width=120, height=20)
        tk.Label(frame, text='Fecha entrega: ').place(x=250, y=32, width=100, height=10)
        new_date_entrega = tk.Entry(frame, textvariable=tk.StringVar(self.ventana_clientes_edit, value=date_entrega))
        new_date_entrega.place(x=340, y=30, width=120, height=20)
        tk.Label(frame, text='Anticipo: ').place(x=250, y=62, width=100, height=10)
        new_anticipo = tk.Entry(frame, textvariable=tk.StringVar(self.ventana_clientes_edit, value=anticipo))
        new_anticipo.place(x=340, y=60, width=120, height=20)
        btn_ce = ttk.Button(self.ventana_clientes_edit, text='Actualizar',
                            command=lambda: self.actualizarCliente(name, celular, pedido, date_pedido, date_entrega,
                                                                   anticipo, new_name.get(), new_celular.get(),
                                                                   new_pedido.get(), new_date_pedido.get(),
                                                                   new_date_entrega.get(), new_anticipo.get()))
        btn_ce.place(x=200, y=107, width=100, height=30)

    def actualizarCliente(self, name, celular, pedido, date_pedido, date_entrega, anticipo, new_name, new_celular,
                          new_pedido, new_date_pedido, new_date_entrega, new_anticipo):
        query = ('UPDATE customers SET name=?, phone=?, delivery=?, date_pedido=?, date_entrega=?, anticipo=? '
                 'WHERE name=? AND celular=? AND pedido=? AND date_pedido=? AND date_entrega=? AND anticipo=?')
        parameters = (
            new_name, new_celular, new_pedido, new_date_pedido, new_date_entrega, new_anticipo, name, celular, pedido,
            date_pedido, date_entrega, anticipo)
        self.run_query_customers(query, parameters)
        self.ventana_clientes_actualizar()
        self.ventana_clientes_edit.destroy()

    def add_user(self):
        windows_add_user = tk.Toplevel()
        windows_add_user.geometry('540x300')
        windows_add_user.resizable(False, False)
        windows_add_user.title('Características de usuarios')
        frame = tk.LabelFrame(windows_add_user, text='Añadir usuario')
        frame.place(x=0, y=0, width=500, height=100)
        frame.grid(row=2, column=2)
        tk.Label(frame, text='Usuario:').grid(row=0, column=0)
        self.user = tk.Entry(frame, textvariable=tk.StringVar(windows_add_user))
        self.user.grid(row=0, column=1)
        self.user.focus()
        tk.Label(frame, text='Contraseña:').grid(row=1, column=0)
        self.password = tk.Entry(frame, textvariable=tk.StringVar(windows_add_user, value=''), show='*')
        self.password.grid(row=1, column=1)
        ttk.Button(frame, text='+',
                   command=lambda: self.agregarU(self.user.get(), self.password.get())).grid(row=2, column=0)

        frame_users = tk.LabelFrame(windows_add_user, text='Usuarios')
        frame_users.place(x=0, y=110, width=500, height=200)
        self.tree_users = ttk.Treeview(frame_users, height=2, columns=('user', 'password'))
        self.tree_users.place(x=0, y=0, width=480, height=130)

        self.tree_users.heading('#0', text='Usuario', anchor=tk.CENTER)
        self.tree_users.heading('#1', text='Contraseña', anchor=tk.CENTER)

        scrollbarU = ttk.Scrollbar(windows_add_user, orient=tk.VERTICAL, command=self.troo.yview)
        scrollbarU.place(x=505, y=90, width=30, height=200)
        self.tree_users.configure(yscrollcommand=scrollbarU.set)

        self.update_table_user()

        ttk.Button(frame_users, text='Editar').place(x=0, y=130, width=240, height=30)
        ttk.Button(frame_users, text='Eliminar').place(x=240, y=130, width=240, height=30)

    def run_queryUsuarios(self, query, parameters=()):
        with sqlite3.connect(self.db_users) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def update_table_user(self):
        records = self.tree_users.get_children()
        for element in records:
            self.tree_users.delete(element)

        query = 'select id, user, password from users'
        db_rows = self.run_queryUsuarios(query)
        for row in db_rows:
            password_hide = ['*' * len(row[2])]
            self.tree_users.insert('', 0, text=row[1], values=password_hide)

    def agregarU(self, user, password):

        self.user.delete(0, tk.END)
        self.password.delete(0, tk.END)
        query = 'insert into users (id, user, password) values (NULL, ?, ?)'
        parameters = (user, password)
        self.run_queryUsuarios(query, parameters)
        self.update_table_user()

    def destroy_window(self):
        try:
            self.edit_wind.destroy()
        except:
            try:
                self.authorization_wind.destroy()
            except:
                try:
                    self.edit_rembolso.destroy()
                except:
                    return

    # CORTE DE CAJA
    def corteCaja(self, usuario, total, dinero):

        self.wind_corteCaja = tk.Toplevel()
        self.wind_corteCaja.geometry('400x200')
        self.wind_corteCaja.resizable(False, False)
        self.wind_corteCaja.title('corte')

        #
        frame = tk.LabelFrame(self.wind_corteCaja, text='Tabla de compras')
        frame.place(x=0, y=0, width=400, height=120)

        nameUsuario = tk.StringVar(value=usuario)
        tk.Entry(frame, textvariable=nameUsuario, state='readonly').place(x=5, y=5)
        tk.Label(frame, text='Total de caja', fg='blue').place(x=5, y=30, width=141, height=30)
        tk.Entry(frame, textvariable=total, fg='blue', state='readonly').place(x=162, y=30, width=120, height=30)

        #
        dinero = float(dinero)
        self.dinero_caja = tk.DoubleVar(value=0)
        self.dinero_caja.set(dinero)
        self.dinero_caja.set(self.total_caja.get() - self.dinero_caja.get())
        tk.Label(frame, text='Dinero ganado', fg='blue').place(x=5, y=60, width=141, height=30)
        tk.Entry(frame, textvariable=self.dinero_caja,
              fg='blue', state='readonly').place(x=162, y=60, width=120, height=30)

        ttk.Button(frame, text='cierre', command=lambda: self.guardarCorte(dinero)).place(x=290, y=60, width=94,
                                                                                          height=30)

    def guardarCorte(self, money):
        data = 'history'
        if not os.path.exists('history'):
            os.makedirs('history')

        date = datetime.datetime.now()
        date_month = str(date.month)
        date_day = str(date.day)
        date_year = str(date.year)
        date_hour = str(date.hour)
        date_minute = str(date.minute)
        if not (os.path.exists(
                data + '/' + 'history_' + date_day + '_' + date_month + '_' + date_year + '_' + date_hour +
                '_' + date_minute + '.txt')):
            file = open(
                'history_' + date_day + '_' + date_month + '_' + date_year + '_' + date_hour + '_' + date_minute +
                '.txt', 'w')
            file.write(str(self.user.get()))
            records = self.tree_historial.get_children()
            query = 'select id, name, price, date, sale from history'
            db_rows = self.run_query_history(query)
            for row in db_rows:
                file.write(':\n')
                file.write(str(row))
            file.write('\nTotal: ')
            file.write(str(self.dinero_caja.get()))
            file.close()
            shutil.move(
                'history_' + date_day + '_' + date_month + '_' + date_year + '_' + date_hour + '_' + date_minute +
                '.txt', data)
            self.borrar_historial(money)

    def table_history_old(self):
        # interfaz de abrir archivo
        nombreArchivo = filedialog.askopenfilename(title='Seleccionar un archivo',
                                                      filetypes=(('txt file', '*.txt'), ('todos los archivos', '*.*')))
        if nombreArchivo != '':
            archivo = open(nombreArchivo, 'r')
            text_list = archivo.readlines()
            archivo.close()
            self.wind_historialOld = tk.Toplevel()
            self.wind_historialOld.geometry('820x400')
            self.wind_historialOld.resizable(False, False)
            self.wind_historialOld.title('Historiales pasados')
            self.treeOld = ttk.Treeview(self.wind_historialOld, height=0, columns=0)
            self.treeOld.place(x=10, y=10, width=800, height=500)
            self.treeOld.heading('#0', text='Ventas del dia', anchor=tk.CENTER)

            self.scrollbarOOld = ttk.Scrollbar(self.wind_historialOld, orient=tk.VERTICAL, command=self.treeOld.yview)
            self.scrollbarOOld.place(x=790, y=10, width=30, height=500)
            self.treeOld.configure(yscrollcommand=self.scrollbarOOld.set)

            for row in text_list:
                self.treeOld.insert('', 0, text=row)


# USUARIOS
def input_users(user, password, conf_user, conf_password, money, window_pas):
    window_pas.message = tk.Label(text='', fg='red')
    window_pas.message.pack()
    try:
        money = float(money)
    except:
        window_pas.message['text'] = 'Ingrese mas dinero'
        return
    i = 0
    for name in conf_user:
        i += 1
        if user == name:
            if password == conf_password[i - 1]:
                window_pas.destroy()
                window = tk.Tk()
                window.geometry('1350x700')
                application = Product(window, user, money)
                window.mainloop()
            else:
                window_pas.message['text'] = '{} no tiene esta contraseña'.format(user)
                break


def run_query_users(query, parameters=()):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result


def main():
    database.create_database()
    database.create_database_customers()
    database.create_database_sales()
    database.create_database_history()
    database.create_database_users()
    window_pas = tk.Tk()
    window_pas.geometry('500x250')
    window_pas.title('Inicio Sesión')
    window_pas.resizable(False, False)
    query = 'select id, user , password from users'
    db_rows = run_query_users(query)
    users_box = ['admin']
    password_box = ['admin']

    for row in db_rows:
        users_box.append(row[1])
        password_box.append(row[2])

    tk.Label(window_pas, text='Usuario').pack()
    user = ttk.Combobox(window_pas, state='readonly')
    user['values'] = users_box
    user.current(0)
    user.pack()

    tk.Label(window_pas, text='Contraseña').pack()
    password = tk.Entry(window_pas, textvariable=tk.StringVar(window_pas, value=''), show='*')
    password.pack()
    password.focus()

    tk.Label(window_pas, text='Dinero en caja').pack()
    money = tk.Entry(window_pas, textvariable=tk.StringVar(window_pas, value='0'))
    money.pack()

    ttk.Button(window_pas, text='Ingresar',
               command=lambda: input_users(user.get(), password.get(), users_box, password_box, money.get(),
                                           window_pas)).pack()

    window_pas.mainloop()


if __name__ == '__main__':
    main()
