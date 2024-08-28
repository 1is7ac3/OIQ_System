"""Import librerías"""
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import datetime
import shutil
import os
import database
import data


class Product():
    """Clase producto"""

    def __init__(self, window, user, money):
        self.wind = window
        self.wind.title("Inventario")
        self.s_height = self.wind.winfo_screenheight()
        self.s_width = self.wind.winfo_screenwidth()
        self.total = tk.DoubleVar(value=0)
        self.total_show = tk.DoubleVar(value=0)
        self.total_exit = tk.DoubleVar(value=0)
        self.total_exit_show = tk.DoubleVar(value=0)
        self.deposito = tk.DoubleVar(value=0)
        self.cambio = tk.DoubleVar(value=0)
        self.dinero_caja = tk.DoubleVar(value=0)
        self.user = tk.StringVar(value=user)
        self.key = tk.StringVar()
        self.total_caja = tk.DoubleVar(value=0)
        self.ubic = ["Rendic", "Bodega1", "Bodega2"]
        tm = datetime.datetime.now()
        self.date = [tk.IntVar(value=tm.day), tk.IntVar(value=tm.hour),
                     tk.IntVar(value=tm.minute),]
        menubar = tk.Menu(self.wind)
        self.wind.config(menu=menubar)
        file_corte = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Usuario", menu=file_corte)
        file_corte.add_command(
            label="cierre de caja",
            command=lambda: self.historial_ventas(money, user))
        file_corte.add_separator()
        file_corte.add_command(label="Agregar usuario", command=self.add_user)
        file_corte.add_command(label="Eliminar usuario")
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir un historial",
                              command=self.table_history_old)
        file_menu.add_command(
            label="Importar Inventario CVS",
            command=lambda: self.confirm_authorization(2),)
        file_menu.add_command(label="Exportar Inventario CVS",
                              command=lambda: self.confirm_authorization(4),)
        file_menu.add_command(label="Cambios en base de datos",
                              command=database.change)
        file_menu.add_separator()
        file_menu.add_command(label="Cerrar sesión", command=self.wind.quit)
        frame = tk.LabelFrame(self.wind, text="Inventario Productos")
        frame.place(x=0, y=0, width=self.s_width, height=self.s_height/10)
        tk.Label(frame, text="Nombre:").place(x=0, y=0)
        self.name = tk.Entry(frame)
        self.name.focus()
        self.name.place(x=55, y=0, width=500)
        tk.Label(frame, text="Precio:").place(x=555, y=0)
        self.price = tk.Entry(frame, textvariable=tk.DoubleVar(value=0))
        self.price.place(x=600, y=0, width=130)
        tk.Label(frame, text="Cantidad:").place(x=740, y=0)
        self.quantity = tk.Entry(frame, textvariable=tk.DoubleVar(value=1))
        self.quantity.place(x=800, y=0, width=100)
        tk.Label(frame, text="Ganancia:").place(x=0, y=30)
        self.gain = tk.Entry(frame, textvariable=tk.DoubleVar(value=30))
        self.gain.place(x=70, y=30, width=30)
        tk.Label(frame, text="Ubicación:").place(x=100, y=30)
        self.location = ttk.Combobox(frame, state="readonly", values=self.ubic)
        self.location.current(0)
        self.location.place(x=170, y=30, width=150)
        tk.Label(frame, text="Código:").place(x=320, y=30)
        self.code = tk.Entry(frame)
        self.code.place(x=370, y=30)
        ttk.Button(frame, text="Guardar producto",
                   command=self.add_product).place(x=600, y=30)
        ttk.Button(frame, text="Atualizar lista",
                   command=self.update_table).place(x=750, y=30)
        self.message = tk.Label(text="", fg="black")
        self.message.place(x=0, y=80, width=781, height=30)
        tree_w = int(self.s_width / 2)
        tree_h = int(self.s_height / 2)
        self.tree = ttk.Treeview(self.wind, columns=(
            "item", "code", "name", "quantity", "price_buy", "price_sale",
            "ganancia", "local1", "local2"))
        self.tree.place(x=0, y=110, width=tree_w, height=tree_h)
        self.tree.column("#0", width=int(tree_w/15), anchor=tk.CENTER)
        self.tree.heading("#0", text="Item", anchor=tk.CENTER)
        self.tree.column("#1", width=int(tree_w/15), anchor=tk.CENTER)
        self.tree.heading("#1", text="Código", anchor=tk.CENTER)
        self.tree.column("#2", width=int(tree_w/4))
        self.tree.heading("#2", text="Descripción", anchor=tk.CENTER)
        self.tree.column("#3", width=int(tree_w/15), anchor=tk.CENTER)
        self.tree.heading("#3", text="Cantidad", anchor=tk.CENTER)
        self.tree.column("#4", width=int(tree_w/9), anchor=tk.CENTER)
        self.tree.heading("#4", text="Precio Compra", anchor=tk.CENTER)
        self.tree.column("#5", width=int(tree_w/12), anchor=tk.CENTER)
        self.tree.heading("#5", text="% Ganancia", anchor=tk.CENTER)
        self.tree.column("#6", width=int(tree_w/10), anchor=tk.CENTER)
        self.tree.heading("#6", text="Precio Venta", anchor=tk.CENTER)
        self.tree.column("#7", width=int(tree_w/12), anchor=tk.CENTER)
        self.tree.heading("#7", text="Rendic", anchor=tk.CENTER)
        self.tree.column("#8", width=int(tree_w/12), anchor=tk.CENTER)
        self.tree.heading("#8", text="Bodega 1", anchor=tk.CENTER)
        self.tree.column("#9", width=int(tree_w/12), anchor=tk.CENTER)
        self.tree.heading("#9", text="Bodega 2", anchor=tk.CENTER)
        self.scroll_bar = ttk.Scrollbar(
            self.wind, orient=tk.VERTICAL, command=self.tree.yview)
        self.scroll_bar.place(x=tree_w, y=120, width=30, height=tree_h)
        self.tree.configure(yscrollcommand=self.scroll_bar.set)
        self.update_table()
        ttk.Button(text="Eliminar",
                   command=lambda: self.confirm_authorization(1)).place(
                       x=0, y=tree_h+120, width=180, height=30)
        ttk.Button(text="Editar",
                   command=lambda: self.confirm_authorization(3)).place(
            x=180, y=tree_h+120, width=180, height=30)
        tk.Label(self.wind, text="Total valor Inventario:").place(
            x=360, y=tree_h+120)
        tk.Label(self.wind, text="$").place(x=500, y=tree_h+120)
        tk.Label(self.wind, textvariable=self.total_show).place(
            x=510, y=tree_h+120)
        tk.Label(self.wind, text="Filtro Descripción:").place(
            x=0, y=tree_h+170)
        self.entry_s_var = tk.StringVar()
        self.entry_s = tk.Entry(self.wind,
                                textvariable=self.entry_s_var)
        self.entry_s.place(x=120, y=tree_h+170, width=200, height=30)
        self.entry_s_var.trace_add("write", self.search)
        self.entry_s_var2 = tk.StringVar()
        self.entry_s2 = tk.Entry(
            self.wind, textvariable=self.entry_s_var2)
        self.entry_s2.place(x=320, y=tree_h+170, width=200, height=30)
        self.entry_s_var2.trace_add("write", self.search)
        tk.Label(self.wind, text="Filtro por código:").place(
            x=0, y=tree_h+200)
        self.entry_s_code_var = tk.StringVar()
        self.entry_s_code = tk.Entry(
            self.wind, textvariable=self.entry_s_code_var)
        self.entry_s_code.place(x=120, y=tree_h+200, width=200, height=30)
        self.entry_s_code_var.trace_add('write', self.search_code)
        frame_shopping = tk.LabelFrame(
            self.wind, text="Productos en salida de inventario")
        frame_shopping.place(x=tree_w+30, y=110,
                             width=int(tree_w/2), height=tree_h)
        self.troo = ttk.Treeview(self.wind, columns=("product", "price"))
        self.troo.place(x=tree_w+30, y=110, width=int(tree_w/2), height=tree_h)
        self.troo.column("#0", width=200, anchor=tk.CENTER)
        self.troo.heading("#0", text="Producto", anchor=tk.CENTER)
        self.troo.column("#1", anchor=tk.CENTER, width=80)
        self.troo.heading("#1", text="Cantidad", anchor=tk.CENTER)
        self.troo.column("#2", anchor=tk.CENTER, width=80)
        self.troo.heading("#2", text="Precio", anchor=tk.CENTER)
        self.scrollbar = ttk.Scrollbar(self.wind, orient=tk.VERTICAL,
                                       command=self.troo.yview)
        x_scroll = int(tree_w+30+tree_w/2)
        self.scrollbar.place(x=x_scroll, y=120, width=30, height=tree_h)
        self.troo.configure(yscrollcommand=self.scrollbar.set)
        ttk.Button(text="retirar", command=self.cobrar).place(
            x=tree_w+20, y=tree_h+120, width=100, height=30)
        ttk.Button(text="Eliminar",
                   command=lambda: self.delete_exit(self.troo.selection()),
                   ).place(x=tree_w+120, y=tree_h+120, width=120, height=30)
        ttk.Button(text="+",
                   command=lambda: self.add_product_exit(self.tree.selection())
                   ).place(x=tree_w+240, y=tree_h+120, width=20, height=30)
        self.quality_exit = tk.Entry(textvariable=tk.IntVar(value=1))
        self.quality_exit.place(
            x=tree_w+270, y=tree_h+120, width=50, height=30)
        self.ubic_exit = ttk.Combobox(state="readonly", values=self.ubic)
        self.ubic_exit.current(0)
        self.ubic_exit.place(x=tree_w+320, y=tree_h+120, width=70, height=30)
        self.message_sales = tk.Label(text="", fg="black", wraplength=200)
        self.message_sales.place(x=tree_w, y=tree_h+150, width=280, height=50)
        self.update_table_sales()
        tk.Label(self.wind, text="Total:").place(x=tree_w, y=tree_h+200)
        tk.Label(self.wind, text="$").place(x=tree_w+70, y=tree_h+200)
        tk.Label(self.wind, textvariable=self.total_exit_show).place(
            x=tree_w+100, y=tree_h+200)
        ttk.Button(text="Ventas del dia",
                   command=lambda: self.historial_ventas(money, user)
                   ).place(x=tree_w, y=tree_h+270, width=300, height=30)

    def search(self, *args):
        """función búsqueda producto"""
        item_tree = self.tree.get_children()
        search = self.entry_s_var.get().upper()
        search2 = self.entry_s_var2.get().upper()
        for item in item_tree:
            if search == "" and search2 == "":
                self.update_table()
            search_name = str(self.tree.item(item)["values"][1])
            if search in search_name and search2 in search_name:
                search_var = self.tree.item(item)
                self.tree.delete(item)
                if float(search_var["values"][2]) < 1:
                    self.tree.insert("", 0, text=search_var["text"], values=(
                        search_var["values"][0], search_var["values"][1],
                        search_var["values"][2], search_var["values"][3],
                        search_var["values"][4], search_var["values"][5],
                        search_var["values"][6], search_var["values"][7],
                        search_var["values"][8],), tags="bg_red",)
                    self.tree.tag_configure("bg_red", background="red")
                elif float(search_var["values"][2]) > 1:
                    self.tree.insert("", 0, text=search_var["text"], values=(
                        search_var["values"][0], search_var["values"][1],
                        search_var["values"][2], search_var["values"][3],
                        search_var["values"][4], search_var["values"][5],
                        search_var["values"][6], search_var["values"][7],
                        search_var["values"][8],), tags="bg_green",)
                    self.tree.tag_configure("bg_green", background="#48E120")
                else:
                    self.tree.insert("", 0, text=search_var["text"], values=(
                        search_var["values"][0], search_var["values"][1],
                        search_var["values"][2], search_var["values"][3],
                        search_var["values"][4], search_var["values"][5],
                        search_var["values"][6], search_var["values"][7],
                        search_var["values"][8],), tags="bg_yellow",)
                    self.tree.tag_configure("bg_yellow", background="yellow")
            self.tree.selection_set(self.tree.get_children()[0])

    def search_code(self, *args):
        """función búsqueda producto"""
        item_tree = self.tree.get_children()
        search = self.entry_s_code_var.get().upper()
        for item in item_tree:
            if search == "":
                self.update_table()
            search_code = str(self.tree.item(item)["values"][0])
            if search in search_code:
                search_var = self.tree.item(item)
                self.tree.delete(item)
                if float(search_var["values"][2]) < 1:
                    self.tree.insert("", 0, text=search_var["text"], values=(
                        search_var["values"][0], search_var["values"][1],
                        search_var["values"][2], search_var["values"][3],
                        search_var["values"][4], search_var["values"][5],
                        search_var["values"][6], search_var["values"][7],
                        search_var["values"][8],), tags="bg_red",)
                    self.tree.tag_configure("bg_red", background="red")
                elif float(search_var["values"][2]) > 1:
                    self.tree.insert("", 0, text=search_var["text"], values=(
                        search_var["values"][0], search_var["values"][1],
                        search_var["values"][2], search_var["values"][3],
                        search_var["values"][4], search_var["values"][5],
                        search_var["values"][6], search_var["values"][7],
                        search_var["values"][8],), tags="bg_green",)
                    self.tree.tag_configure("bg_green", background="#48E120")
                else:
                    self.tree.insert("", 0, text=search_var["text"], values=(
                        search_var["values"][0], search_var["values"][1],
                        search_var["values"][2], search_var["values"][3],
                        search_var["values"][4], search_var["values"][5],
                        search_var["values"][6], search_var["values"][7],
                        search_var["values"][8],), tags="bg_yellow",)
                    self.tree.tag_configure("bg_yellow", background="yellow")
            self.tree.selection_set(self.tree.get_children()[0])

    def update_table(self):
        """función actualizar tabla"""
        self.total.set(value=0)
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = """select id, code, name, price_buy, ganancia, price_sales,
        location, location2, location3 from product order by name desc"""
        db_rows = database.run_query(query)
        i = 0
        for row in db_rows:
            q_t = row[6]+row[7]+row[8]
            self.total.set(self.total.get() + (q_t * row[4]))
            self.total_show.set(format(self.total.get(), ","))
            i += 1
            style = ttk.Style()
            style.configure("border_color", background="black")
            if q_t < 1:
                self.tree.insert("", 0, text=str(i),
                                 values=(row[1], row[2], q_t, row[3],
                                         row[4], row[5], row[6], row[7], row[8]
                                         ), tags="bg_red",)
                self.tree.tag_configure("bg_red", background="red")
            elif (q_t) > 1:
                self.tree.insert("", 0, text=str(i),
                                 values=(row[1], row[2], q_t, row[3],
                                         row[4], row[5], row[6], row[7], row[8]
                                         ), tags="bg_green",)
                self.tree.tag_configure("bg_green", background="#48E120")
            else:
                self.tree.insert("", 0, text=str(i),
                                 values=(row[1], row[2], q_t, row[3],
                                         row[4], row[5], row[6], row[7], row[8]
                                         ), tags="bg_yellow",)
                self.tree.tag_configure("bg_yellow", background="yellow")

    def update_table_sales(self):
        """función actualizar tabla de salida"""
        self.total_exit.set(value=0)
        self.total_exit_show.set(value=0)
        records = self.troo.get_children()
        for element in records:
            self.troo.delete(element)
        query = "select id, name, quantity, price from sales"
        db_rows = database.run_query_sqlite3(query)
        for row in db_rows:
            self.total_exit.set(self.total_exit.get() + (row[2] * row[3]))
            self.total_exit_show.set(format(self.total_exit.get(), ","))
            self.troo.insert("", 0, text=row[1], values=(row[2], row[3]))

    def validation(self):
        """funcion validacion nombre y precio"""
        if len(self.name.get()) != 0 and len(self.price.get()) != 0:
            return True
        return False

    def validation_duplicate(self):
        """funcion validar que los datos sean numeros"""
        if self.price.get().isdigit() and self.quantity.get().isdigit():
            return 1
        return 2

    def add_product(self):
        """funcion agregar producto al inventario"""
        if self.validation():
            option = self.validation_duplicate()
            if option == 1:
                try:
                    price = round(float(self.price.get()))
                    quantity = round(float(self.quantity.get()))
                    gain = round(float(self.gain.get()))
                    price_sale = round(price * (1 + (float(gain) / 100)))
                    code = str(self.code.get().upper())
                    name = str(self.name.get().upper())
                    location = self.location.current()
                    print(self.location.current())
                    if location == 0:
                        query = """insert into product (code, name, price_buy,
                    ganancia, price_sales, location ,location2, location3)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)"""
                        parameters = (code, name, price, gain, price_sale,
                                      quantity, 0, 0)
                    elif location == 1:
                        query = """insert into product (code, name, price_buy,
                    ganancia, price_sales, location ,location2, location3)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)"""
                        parameters = (code, name, price, gain, price_sale, 0,
                                      quantity, 0)
                    elif location == 2:
                        query = """insert into product (code, name, price_buy,
                    ganancia, price_sales, location ,location2, location3)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)"""
                        parameters = (code, name, price, gain, price_sale, 0,
                                      0, quantity)
                    database.run_query_edit(query, parameters)
                    self.message["text"] = f"{self.name.get()} agregado"
                    self.name.delete(0, tk.END)
                    self.price.delete(0, tk.END)
                    self.quantity.delete(0, tk.END)
                    self.location.delete(0, tk.END)
                    self.code.delete(0, tk.END)
                    self.update_table()
                except database.maria.errors.IntegrityError:
                    self.message["text"] = f"{self.name.get()} esta incluido"
            if option == 2:
                self.message["text"] = "Verificar que los datos sean correctos"
        else:
            self.message["text"] = "El nombre y el precio son requeridos."

    def add_product_exit(self, id_data):
        """función agregar producto salida de inventario"""
        self.message_sales["text"] = ""
        try:
            self.tree.item(id_data)["text"]
        except IndexError:
            self.message_sales["text"] = "por favor seleccione un producto."
            return
        cantidad = int(self.tree.item(id_data)["values"][2])
        if not self.quality_exit.get().isdigit():
            self.message_sales["text"] = "Valor incorrecto en cantidad."
        elif cantidad < int(self.quality_exit.get()):
            self.message_sales["text"] = "No hay suficiente producto."
        elif cantidad >= int(self.quality_exit.get()):
            try:
                query = """insert into sales (name, quantity, price)
                values (%s, %s, %s)"""
                name = self.tree.item(id_data)["values"][1]
                quantity = self.quality_exit.get()
                price = self.tree.item(id_data)["values"][5]
                parameters = (name, quantity, price)
                database.run_query_edit_sqlite3(query, parameters)
                self.message_sales["text"] = f"Producto {name} fue agregado"
                self.update_table_sales()
            except database.sqlite3.IntegrityError as err:
                if err.args[0] == 'UNIQUE constraint failed':
                    self.message_sales["text"] = f"""{err}: ya se encuentra
                    en agregado."""
                self.message_sales["text"] = f"{err}"

    def delete_product(self, id_data):
        """funcion delete product"""
        self.message["text"] = ""
        try:
            self.tree.item(id_data)["values"][1]
        except IndexError:
            self.message["text"] = "por favor seleccione un producto"
            return
        self.message["text"] = ""
        name = self.tree.item(id_data)["values"][1]
        query = "DELETE FROM product WHERE name = %s"
        database.run_query_edit(query, (name,))
        self.message["text"] = f"El dato {name} fue eliminado correctamente"
        self.update_table()

    def delete_exit(self, id_data):
        """funcion eliminar de salida inventario"""
        self.message_sales["text"] = ""
        try:
            self.troo.item(id_data)["text"][0]
        except IndexError:
            self.message_sales["text"] = "por favor seleccione un producto"
            return
        self.message_sales["text"] = ""
        name = self.troo.item(id_data)["text"]
        query = "DELETE FROM sales WHERE name = %s"
        database.run_query_edit_sqlite3(query, (name,))
        self.message_sales["text"] = f"{name} fue eliminado correctamente"
        self.update_table_sales()

    def confirm_authorization(self, option):
        """funcion confirmar contraseña"""
        self.authorization_wind = tk.Toplevel()
        self.authorization_wind.geometry("500x210")
        self.authorization_wind.resizable(False, False)
        tk.Label(self.authorization_wind, text="contraseña principal").pack()
        clave = tk.Entry(
            self.authorization_wind,
            textvariable=tk.StringVar(self.authorization_wind, value=""),
            show="*",)
        clave.pack()
        clave.focus()
        tk.Button(self.authorization_wind, text="Ingresar",
                  command=lambda: self.verify_key(clave.get(), option),
                  ).pack()

    def verify_key(self, key, option):
        """funcion clave de verificacion"""
        self.authorization_wind.destroy()
        if key != "":
            if key == data.PASSWORD_ROOT:
                if option == 1:
                    self.delete_product(self.tree.selection())
                if option == 2:
                    self.import_lote()
                if option == 3:
                    self.edit_product(self.tree.selection())
                if option == 4:
                    self.export_lote()
        else:
            messagebox.showwarning("Error", "Contraseña incorrecta")
            self.authorization_wind.destroy()

    def edit_product(self, id_data):
        """funcion editar producto"""
        self.message["text"] = ""
        try:
            self.tree.item(id_data)["text"][0]
        except IndexError:
            self.message["text"] = "por favor seleccione un producto"
            return
        old_code = self.tree.item(id_data)["values"][0]
        old_name = self.tree.item(id_data)["values"][1]
        old_location2 = self.tree.item(id_data)["values"][7]
        old_price_buy = self.tree.item(id_data)["values"][3]
        old_ganancia = self.tree.item(id_data)["values"][4]
        old_location3 = self.tree.item(id_data)["values"][8]
        old_location = self.tree.item(id_data)["values"][6]
        edit_wind = tk.Toplevel()
        edit_wind.geometry("500x500")
        edit_wind.resizable(False, False)
        tk.Label(edit_wind, text="Nombre").grid(row=0, column=1)
        tk.Entry(
            edit_wind,
            textvariable=tk.StringVar(edit_wind, value=old_name),
            state="readonly",
        ).grid(row=0, column=2, ipadx=100)
        tk.Label(edit_wind, text="Cambio nombre").grid(row=1, column=1)
        new_name = tk.Entry(
            edit_wind, textvariable=tk.StringVar(edit_wind, value=old_name)
        )
        new_name.grid(row=1, column=2, ipadx=100)
        tk.Label(edit_wind, text="Precio compra").grid(row=2, column=1)
        tk.Entry(
            edit_wind,
            textvariable=tk.StringVar(edit_wind, value=old_price_buy),
            state="readonly",
        ).grid(row=2, column=2, ipadx=100)
        tk.Label(edit_wind, text="Cambio precio").grid(row=3, column=1)
        new_price_buy = tk.Entry(
            edit_wind, textvariable=tk.StringVar(
                edit_wind, value=old_price_buy)
        )
        new_price_buy.grid(row=3, column=2, ipadx=100)
        tk.Label(edit_wind, text="Bodega1").grid(row=4, column=1)
        tk.Entry(
            edit_wind,
            textvariable=tk.StringVar(edit_wind, value=old_location2),
            state="readonly",
        ).grid(row=4, column=2, ipadx=100)
        tk.Label(edit_wind, text="Cambio Bodega1").grid(row=5, column=1)
        new_location2 = tk.Entry(
            edit_wind, textvariable=tk.StringVar(edit_wind,
                                                 value=old_location2))
        new_location2.grid(row=5, column=2, ipadx=100)
        tk.Label(edit_wind, text="Código").grid(row=6, column=1)
        tk.Entry(
            edit_wind,
            textvariable=tk.StringVar(edit_wind, value=old_code),
            state="readonly",
        ).grid(row=6, column=2, ipadx=100)
        tk.Label(edit_wind, text="Cambio código").grid(row=7, column=1)
        new_code = tk.Entry(
            edit_wind, textvariable=tk.StringVar(edit_wind, value=old_code)
        )
        new_code.grid(row=7, column=2, ipadx=100)
        tk.Label(edit_wind, text="Ganancia").grid(row=8, column=1)
        tk.Entry(
            edit_wind,
            textvariable=tk.StringVar(edit_wind, value=old_ganancia),
            state="readonly",
        ).grid(row=8, column=2, ipadx=100)
        tk.Label(edit_wind, text="Cambio Ganancia").grid(row=9, column=1)
        new_ganancia = tk.Entry(
            edit_wind, textvariable=tk.StringVar(edit_wind, value=old_ganancia)
        )
        new_ganancia.grid(row=9, column=2, ipadx=100)
        tk.Label(edit_wind, text="Rendic").grid(row=10, column=1)
        tk.Entry(
            edit_wind,
            textvariable=tk.StringVar(edit_wind, value=old_location),
            state="readonly",
        ).grid(row=10, column=2, ipadx=100)
        tk.Label(edit_wind, text="Cambio Rendic").grid(row=11, column=1)
        new_location = tk.Entry(
            edit_wind, textvariable=tk.StringVar(edit_wind, value=old_location)
        )
        new_location.grid(row=11, column=2, ipadx=100)
        tk.Label(edit_wind, text="Bodega2").grid(row=12, column=1)
        tk.Entry(
            edit_wind,
            textvariable=tk.StringVar(edit_wind, value=old_location3),
            state="readonly",).grid(row=12, column=2, ipadx=100)
        tk.Label(edit_wind, text="Cambio Bodega2").grid(row=13, column=1)
        new_location3 = tk.Entry(
            edit_wind, textvariable=tk.StringVar(edit_wind, value=old_location)
        )
        new_location3.grid(row=13, column=2, ipadx=100)
        tk.Button(edit_wind, text="Guardar",
                  command=lambda: self.edit_records(
                      new_name.get().upper(), old_name, new_price_buy.get(),
                      old_price_buy, new_location2.get(), old_location2,
                      new_code.get().upper(), old_code, old_ganancia,
                      new_ganancia.get(), old_location,
                      new_location.get().upper(), old_location3,
                      new_location3.get(), edit_wind,),
                  ).grid(row=14, column=2, sticky=tk.W + tk.E)

    def edit_records(self, new_name, old_name, new_price_buy, old_price_buy,
                     new_location2, old_location2, new_code, old_code,
                     old_ganancia, new_ganancia, old_location, new_location,
                     old_location3, new_location3, edit_wind,):
        """funcion editar productos"""
        new_price_sale = float(new_price_buy) * \
            (1 + (float(new_ganancia) / 100))
        query = """UPDATE product SET code=%s, name=%s, price_buy=%s,
        ganancia=%s, price_sales=%s, location=%s , location2=%s, location3=%s
        WHERE code=%s AND name=%s AND price_buy=%s AND ganancia=%s
        AND location=%s AND location2=%s AND location3=%s"""
        parameters = (new_code, new_name, new_price_buy, new_ganancia,
                      new_price_sale, new_location, new_location2,
                      new_location3, old_code, old_name, old_price_buy,
                      old_ganancia, old_location, old_location2, old_location3,)
        print(query, parameters)
        database.run_query_edit(query, parameters)
        edit_wind.destroy()
        self.message["text"] = f"El dato {new_name} fue actualizado"
        self.update_table()

    def cobrar(self):
        """funcion retirar de inventario"""
        self.cobrar_wind = tk.Toplevel()
        self.cobrar_wind.geometry("320x200")
        self.cambio.set(value=0)
        tk.Label(self.cobrar_wind, text="TOTAL").grid(row=0, column=0)
        tk.Entry(self.cobrar_wind, textvariable=self.total_exit,
                 state="readonly").grid(row=0, column=1)
        tk.Label(self.cobrar_wind, text="Pago").grid(row=1, column=0)
        self.deposito = tk.Entry(
            self.cobrar_wind, textvariable=self.total_exit)
        self.deposito.grid(row=1, column=1)
        tk.Label(self.cobrar_wind, text="Cambio").grid(row=2, column=0)
        tk.Entry(self.cobrar_wind, textvariable=self.cambio,
                 state="readonly").grid(row=2, column=1)
        tk.Button(self.cobrar_wind, text="Retirar",
                  command=self.change_sales).grid(row=3, column=1,
                                                  sticky=tk.W + tk.E)

    def change_sales(self):
        """funcion salida inventario"""
        diferencia = float(self.deposito.get()) - self.total_exit.get()
        if diferencia >= 0:
            self.cambio.set(diferencia)
            store_list = self.tree.get_children()
            for store_data in store_list:
                product_store = str(self.tree.item(store_data)["values"][1])
                price = int(self.tree.item(store_data)["values"][5])
                if self.ubic_exit.current() == 0:
                    quantity = int(self.tree.item(store_data)["values"][6])
                    ubica = "location"
                elif self.ubic_exit.current() == 1:
                    quantity = int(self.tree.item(store_data)["values"][7])
                    ubica = "location2"
                elif self.ubic_exit.current() == 2:
                    quantity = int(self.tree.item(store_data)["values"][8])
                    ubica = "location3"

                sales_list = self.troo.get_children()
                for sales_data in sales_list:
                    exit_quan = int(self.troo.item(sales_data)["values"][0])
                    sales_product = self.troo.item(sales_data)["text"]
                    if product_store == sales_product:
                        new_quan = quantity - exit_quan
                        if new_quan >= 0:
                            query = f"""UPDATE product SET
                                        {ubica}=%s WHERE name=%s"""
                            parameters = (new_quan, product_store)
                            database.run_query_edit(query, parameters)
                            self.add_product_history(
                                product_store, price, exit_quan, "Venta")

            self.update_table()
            list_venta = self.troo.get_children()
            for dato_venta in list_venta:
                name = self.troo.item(dato_venta)["text"]
                query = "DELETE FROM sales WHERE name=%s"
                database.run_query_edit_sqlite3(query, (name,))
            self.update_table_sales()
        else:
            messagebox.showwarning("Error", "Deposite mas dinero")
        self.cobrar_wind.destroy()

    def add_product_history(self, name, price, quantity, sale):
        """Funcion agregar producto history"""
        query = """insert into history (name, price, quantity, date, sale)
        values(%s, %s, %s, %s, %s)"""
        date = datetime.datetime.now()
        parameters = (name, price, quantity, date, sale)
        database.run_query_edit(query, parameters)

    def update_history(self, dinero):
        """Funcion atualizar historial"""
        records = self.tree_historial.get_children()
        for element in records:
            self.tree_historial.delete(element)
        query = "select id, name, price, date, sale from history"
        db_rows = database.run_query(query)
        dinero = float(dinero)
        self.total_caja.set(dinero)
        for row in db_rows:
            self.tree_historial.insert(
                "", 0, text=row[1], values=(row[2], row[4], row[3])
            )
            if str(row[4]) == "Venta":
                self.total_caja.set(self.total_caja.get() + row[2])

    def historial_ventas(self, dinero, usuario):
        """funcion historial"""
        self.wind_historial = tk.Toplevel()
        self.wind_historial.geometry("1100x400")
        self.wind_historial.resizable(False, False)
        self.wind_historial.title("Historial de ventas")
        self.tree_historial = ttk.Treeview(
            self.wind_historial, height=2, columns=("name", "price", "")
        )
        self.tree_historial.place(x=20, y=10, width=1030, height=300)
        self.tree_historial.heading("#0", text="Producto", anchor=tk.CENTER)
        self.tree_historial.heading("#1", text="Precio", anchor=tk.CENTER)
        self.tree_historial.heading(
            "#2", text="devolución o compra", anchor=tk.CENTER)
        self.tree_historial.heading("#3", text="date", anchor=tk.CENTER)
        scroll_bar_historial = ttk.Scrollbar(
            self.wind_historial, orient=tk.VERTICAL,
            command=self.tree_historial.yview)
        scroll_bar_historial.place(x=1050, y=10, width=20, height=300)
        self.tree_historial.configure(yscrollcommand=scroll_bar_historial.set)
        self.update_history(dinero)
        tk.Label(self.wind_historial, text="TOTAL", fg="blue").place(
            x=20, y=340, width=94, height=30
        )
        tk.Entry(
            self.wind_historial,
            textvariable=self.total_caja,
            state="readonly",
            fg="blue",
        ).place(x=114, y=340, width=94, height=30)
        ttk.Button(
            self.wind_historial,
            text="Corte",
            command=lambda: self.corte_caja(usuario, self.total_caja, dinero),
        ).place(x=930, y=360, width=94, height=30)

    def borrar_historial(self, money):
        """funcion borrar historial"""
        records = self.tree_historial.get_children()
        for element in records:
            name = self.tree_historial.item(element)["text"]
            query = "DELETE FROM history WHERE name=%s"
            database.run_query_edit(query, (name,))
        self.update_history(money)

    def add_user(self):
        """funcion agregar usuario"""
        windows_add_user = tk.Toplevel()
        windows_add_user.geometry("300x300")
        windows_add_user.resizable(False, False)
        windows_add_user.title("Características de usuarios")
        frame = tk.LabelFrame(windows_add_user, text="Añadir usuario")
        frame.place(x=0, y=0, width=500, height=100)
        frame.grid(row=2, column=2)
        tk.Label(frame, text="Usuario:").grid(row=0, column=0)
        self.user = tk.Entry(
            frame, textvariable=tk.StringVar(windows_add_user))
        self.user.grid(row=0, column=1)
        self.user.focus()
        tk.Label(frame, text="Contraseña:").grid(row=1, column=0)
        self.key = tk.Entry(
            frame, textvariable=tk.StringVar(
                windows_add_user, value=""), show="*")
        self.key.grid(row=1, column=1)
        frame_users = tk.LabelFrame(windows_add_user, text="Usuarios")
        frame_users.place(x=0, y=110, width=500, height=200)
        tree_users = ttk.Treeview(
            frame_users, height=2, columns=("user", "password"))
        tree_users.place(x=0, y=0, width=480, height=130)
        tree_users.heading("#0", text="Usuario", anchor=tk.CENTER)
        tree_users.heading("#1", text="Contraseña", anchor=tk.CENTER)
        scrollbar_u = ttk.Scrollbar(
            windows_add_user, orient=tk.VERTICAL, command=self.troo.yview
        )
        scrollbar_u.place(x=505, y=90, width=30, height=200)
        tree_users.configure(yscrollcommand=scrollbar_u.set)
        ttk.Button(
            frame,
            text="+",
            command=lambda: self.add_u(
                self.user.get(), self.key.get(), tree_users),
        ).grid(row=2, column=0)
        self.update_table_user(tree_users)

        ttk.Button(frame_users, text="Editar").place(
            x=0, y=130, width=240, height=30)
        ttk.Button(frame_users, text="Eliminar").place(
            x=240, y=130, width=240, height=30
        )

    def update_table_user(self, tree_users):
        """Funcion tabla usuarios"""
        records = tree_users.get_children()
        for element in records:
            tree_users.delete(element)

        query = "select id, name, password from users"
        db_rows = database.run_query(query)
        for row in db_rows:
            key_hide = ["*" * len(row[2])]
            tree_users.insert("", 0, text=row[1], values=key_hide)

    def add_u(self, user, key, tree_users):
        """Funcion agreager user"""
        self.user.delete(0, tk.END)
        self.key.delete(0, tk.END)
        query = "insert into users (name, password) values (%s, %s)"
        parameters = (user, key)
        database.run_query_edit(query, parameters)
        self.update_table_user(tree_users)

    # CORTE DE CAJA
    def corte_caja(self, usuario, total, dinero):
        """funcion corte caja"""
        wind_corte_caja = tk.Toplevel()
        wind_corte_caja.geometry("400x200")
        wind_corte_caja.resizable(False, False)
        wind_corte_caja.title("corte")
        frame = tk.LabelFrame(wind_corte_caja, text="Tabla de compras")
        frame.place(x=0, y=0, width=400, height=120)
        name_user = tk.StringVar(value=usuario)
        tk.Entry(frame, textvariable=name_user,
                 state="readonly").place(x=5, y=5)
        tk.Label(frame, text="Total de caja", fg="blue").place(
            x=5, y=30, width=141, height=30)
        tk.Entry(frame, textvariable=total, fg="blue", state="readonly").place(
            x=162, y=30, width=120, height=30)
        dinero = float(dinero)
        self.dinero_caja.set(dinero)
        self.dinero_caja.set(self.total_caja.get() - self.dinero_caja.get())
        tk.Label(frame, text="Dinero ganado", fg="blue").place(
            x=5, y=60, width=141, height=30)
        tk.Entry(frame, textvariable=self.dinero_caja, fg="blue",
                 state="readonly").place(x=162, y=60, width=120, height=30)
        ttk.Button(frame, text="cierre",
                   command=lambda: self.save_corte(dinero, wind_corte_caja),
                   ).place(x=290, y=60, width=94, height=30)

    def save_corte(self, money, wind_corte_caja):
        """Funcion guardar corte"""
        data_history = "history"
        if not os.path.exists("history"):
            os.makedirs("history")

        date = datetime.datetime.now()
        date_month = str(date.month)
        date_day = str(date.day)
        date_year = str(date.year)
        date_hour = str(date.hour)
        date_minute = str(date.minute)
        if not (
            os.path.exists(
                data_history
                + "/"
                + "history_"
                + date_day
                + "_"
                + date_month
                + "_"
                + date_year
                + "_"
                + date_hour
                + "_"
                + date_minute
                + ".txt"
            )
        ):
            file = open(
                "history_"
                + date_day
                + "_"
                + date_month
                + "_"
                + date_year
                + "_"
                + date_hour
                + "_"
                + date_minute
                + ".txt",
                "w",
                encoding="utf-8",
            )
            file.write(str(self.user.get()))
            query = "select id, name, price, date, sale from history"
            db_rows = database.run_query(query)
            for row in db_rows:
                file.write(":\n")
                file.write(str(row))
            file.write("\nTotal: ")
            file.write(str(self.dinero_caja.get()))
            file.close()
            shutil.move(
                "history_"
                + date_day
                + "_"
                + date_month
                + "_"
                + date_year
                + "_"
                + date_hour
                + "_"
                + date_minute
                + ".txt",
                data_history,
            )
            self.borrar_historial(money)
        wind_corte_caja.destroy()

    def import_lote(self):
        """funcion import for  lote"""
        name_file = filedialog.askopenfilename(
            title="Seleccionar un archivo",
            filetypes=(("csv file", "*.csv"), ("todos los archivos", "*.*")),
        )
        if name_file != "":
            database.csv_import(name_file)
            self.update_table()

    def export_lote(self):
        """funcion import for  lote"""
        name_file = filedialog.asksaveasfilename(
            title="Seleccionar un archivo",
            filetypes=(("csv file", "*.csv"), ("todos los archivos", "*.*")),
        )
        if name_file != "":
            database.csv_export(name_file)
            self.update_table()

    def table_history_old(self):
        """interfaz de abrir archivo"""
        name_file = filedialog.askopenfilename(
            title="Seleccionar un archivo",
            filetypes=(("Text file", "*.txt"), ("todos los archivos", "*.*")),
        )
        if name_file != "":
            archivo = open(name_file, "r", encoding="utf-8")
            text_list = archivo.readlines()
            archivo.close()
            wind_history_old = tk.Toplevel()
            wind_history_old.geometry("820x400")
            wind_history_old.resizable(False, False)
            wind_history_old.title("Historiales pasados")
            tree_old = ttk.Treeview(wind_history_old, height=0, columns=0)
            tree_old.place(x=10, y=10, width=800, height=500)
            tree_old.heading("#0", text="Ventas del dia", anchor=tk.CENTER)

            scroll_bar_old = ttk.Scrollbar(
                wind_history_old, orient=tk.VERTICAL, command=tree_old.yview
            )
            scroll_bar_old.place(x=790, y=10, width=30, height=500)
            tree_old.configure(yscrollcommand=scroll_bar_old.set)

            for row in text_list:
                tree_old.insert("", 0, text=row)


def input_users(user, key, conf_user, conf_key, money, w_pas):
    """funcion entrada de usuarios"""
    w_pas.message = tk.Label(text="", fg="red")
    w_pas.message.pack()
    i = 0
    for name in conf_user:
        i += 1
        if user == name:
            if key == conf_key[i - 1]:
                w_pas.destroy()
                window = tk.Tk()
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                window.geometry(f"{screen_width}x{screen_height}")

                Product(window, user, money)
                window.mainloop()
            else:
                w_pas.message["text"] = f"{user} contraseña incorrecta"
                break


def main():
    """funcion principal"""
    database.create_database()
    database.create_database_users()
    database.create_table()
    database.create_table_sales()
    database.create_database_history()
    w_pas = tk.Tk()
    screen_width_init = int(w_pas.winfo_screenwidth() / 4)
    screen_height_init = int(w_pas.winfo_screenheight() / 4)
    w_pas.geometry(f"{screen_width_init}x{screen_height_init}")
    w_pas.title("Inicio Sesión")
    w_pas.resizable(False, False)
    query = "select id, name, password from users"
    db_rows = database.run_query(query)
    users_box = ["admin"]
    key_box = ["admin"]

    for row in db_rows:
        users_box.append(row[1])
        key_box.append(row[2])

    tk.Label(w_pas, text="Usuario").pack()
    user = ttk.Combobox(w_pas, state="readonly")
    user["values"] = users_box
    user.current(0)
    user.pack()

    tk.Label(w_pas, text="Contraseña").pack()
    key = tk.Entry(w_pas, textvariable=tk.StringVar(w_pas, value=""), show="*")
    key.pack()
    key.focus()

    tk.Label(w_pas, text="Dinero en caja").pack()
    money = tk.Entry(w_pas, textvariable=tk.StringVar(w_pas, value="0"))
    money.pack()
    ttk.Button(w_pas, text="Ingresar",
               command=lambda: input_users(
                   user.get(), key.get(), users_box, key_box, money.get(),
                   w_pas),).pack()
    key.bind("<Return>", lambda: input_users(
        user.get(), key.get(), users_box, key_box, money.get(), w_pas))
    w_pas.mainloop()


if __name__ == "__main__":
    main()
