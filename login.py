from datetime import datetime
import os
import sys
from openpyxl import Workbook
import data
import ui_history
import ui_login
import ui_inventary
import database
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import ui_edit


class Login(ui_login.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui_login.Ui_sesion()
        self.ui.setupUi(self)
        # eliminar barra
        self.setWindowFlag(ui_login.Qt.FramelessWindowHint)
        # transparente
        self.setAttribute(ui_login.Qt.WA_TranslucentBackground)
        self.ui.b_start.clicked.connect(self.sesion)
        query = "select name, password from users"
        db_rows = database.run_query(query)
        self.users_box = []
        self.key_box = []
        self.int = 1
        for row in db_rows:
            self.users_box.append(row[0])
            self.key_box.append(row[1])
        if len(self.users_box) < 1:
            i_query = "insert into users (name,password) values (%s,%s)"
            user = QtW.QInputDialog.getText(
                None, "Inicializacion", "Introduzca nuevo usuario:")
            key = QtW.QInputDialog.getText(
                None, "Inicializacion", "contraseña:", QtW.QLineEdit.Password)
            i_parameters = (user[0], key[0])
            database.run_query_edit(i_query, i_parameters)
            query = "select name, password from users"
            db_rows = database.run_query(query)
            for row in db_rows:
                self.users_box.append(row[0])
                self.key_box.append(row[1])
        self.ui.i_user.addItems(self.users_box)
        self.ui.i_user.setCurrentIndex(0)
        self.ui.i_key.setFocus()
        self.ui.i_key.setEchoMode(ui_login.QLineEdit.Password)

    def sesion(self):
        self.ui.key_result.setText("")
        i = self.ui.i_user.currentIndex()
        if self.ui.i_key.text() == self.key_box[i]:
            self.close()
            self.window = product(self.users_box[i])
            self.window.show()
        elif self.int < 3:
            self.ui.key_result.setText(f"Contraseña incorrecta {self.int}/3")
            self.int += 1
        else:
            self.close()


class product(ui_inventary.QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.win = ui_inventary.Ui_inventory()
        self.win.setupUi(self)
        self.win.action_i.triggered.connect(lambda: self.auth(2))
        self.win.action_e.triggered.connect(lambda: self.auth(4))
        self.win.action_s.triggered.connect(self.close)
        self.win.action_u.triggered.connect(self.add_user)
        self.win.b_up.clicked.connect(self.update_list)
        self.win.b_add.clicked.connect(self.add_product_exit)
        self.win.b_del.clicked.connect(self.delete_exit)
        self.win.b_fin.clicked.connect(self.charge)
        self.win.action_c.triggered.connect(self.close_local)
        self.user = user
        self.update_list()
        self.update_list_sales()
        self.win.i_fcode.textChanged.connect(self.search_code)
        self.win.i_fdesc.textChanged.connect(self.search_desc)
        self.win.i_fdesc2.textChanged.connect(self.search_desc)
        self.win.b_his.clicked.connect(self.history)
        self.win.b_edit.clicked.connect(lambda: self.auth(3))
        self.win.b_delete.clicked.connect(lambda: self.auth(1))

    def search_code(self):
        self.win.tree.clearSelection()
        for i in range(self.win.tree.topLevelItemCount()):
            item = self.win.tree.topLevelItem(i)
            if self.win.i_fcode.text() == "":
                self.update_list()
            elif self.win.i_fcode.text() in item.text(1):
                item.setHidden(False)
            else:
                item.setHidden(True)

    def search_desc(self):
        search_1 = self.win.i_fdesc.text().upper()
        search_2 = self.win.i_fdesc2.text().upper()
        for i in range(self.win.tree.topLevelItemCount()):
            item = self.win.tree.topLevelItem(i)
            if self.win.i_fdesc.text() == "":
                self.update_list()
            elif search_1 in item.text(2) and search_2 in item.text(2):
                item.setHidden(False)
            else:
                item.setHidden(True)

    def charge(self):
        ubic = self.win.c_local.currentIndex()
        if ubic == 0:
            ubica = "location"
        elif ubic == 1:
            ubica = "location2"
        else:
            ubica = "location3"
        qdata = f"""select name, {ubica} from product"""
        db_rows = database.run_query(qdata)
        for row in db_rows:
            qdata2 = """select name, quantity, price from sales"""
            db_rows2 = database.run_query(qdata2)
            for row2 in db_rows2:
                if row2[0] == row[0]:
                    new_qua = row[1]-row2[1]
                    if new_qua >= 0:
                        query = f"""UPDATE product SET
                                        {ubica}=%s WHERE name=%s"""
                        parameters = (new_qua, row2[0])
                        self.add_history(row2[0], row2[1], row2[2], self.user,
                                         "Venta")
                        database.run_query_edit(query, parameters)
                        query2 = "DELETE FROM sales WHERE name=%s"
                        database.run_query_edit(query2, (row2[0],))
        self.update_list()
        self.update_list_sales()

    def add_history(self, name, quantity, price, user, action):
        """Funcion agregar producto history"""
        query = """insert into history (name, price, quantity, date, user,
        action) values(%s, %s, %s, %s, %s, %s)"""
        date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        parameters = (name, price, quantity, date, user, action)
        database.run_query_edit(query, parameters)

    def import_lote(self):
        """funcion import for  lote"""
        name_file = QtW.QFileDialog.getOpenFileName(
            None, "Abrir archivo", "", "csv file (*.csv)")
        if name_file[0] != "":
            database.csv_import(name_file[0])
            self.update_list()

    def export_lote(self):
        """funcion import for  lote"""
        name_file = QtW.QFileDialog.getSaveFileName(
            None, "Guardar archivo", "", "csv file (*.csv)")
        if name_file[0] != "":
            database.csv_export(name_file[0])
            self.update_list()

    def auth(self, option):
        key = QtW.QInputDialog.getText(None, "Autorizacion",
                                       "Ingrese Contraseña:",
                                       QtW.QLineEdit.Password)
        print(key[0])
        if key[0] == data.PASSWORD_ROOT:
            if option == 1:
                try:
                    id_data = self.win.tree.selectedItems()[0]
                    query = """delete from product where code=%s"""
                    database.run_query_edit(query, (id_data.text(1),))
                    self.win.l_info_exit.setText(f"{id_data.text(2)} Borrado")
                    self.update_list()
                except IndexError:
                    self.win.l_info_exit.setText("Seleccione un producto")
            if option == 2:
                self.import_lote()
            if option == 3:
                self.win_e = Edit(self.win.tree.selectedItems()[0])
                self.win_e.show()
                self.update_list()
            if option == 4:
                self.export_lote()
        else:
            QtW.QMessageBox.warning(None, "Error", "Contraseña Incorrecta")

    def update_list(self):
        self.win.tree.clear()
        t_inventory = 0
        locale = QtC.QLocale(QtC.QLocale.Spanish, QtC.QLocale.Chile)
        self.win.t_inventary.setText(
            locale.toCurrencyString(t_inventory))
        query = """select id, code, name, price_buy, ganancia, price_sales,
            location, location2, location3 from product order by name ASC"""
        db_rows = database.run_query(query)
        item = []
        i = 1
        for row in db_rows:
            q_t = row[6]+row[7]+row[8]
            item.append(ui_inventary.QTreeWidgetItem(
                [str(i), row[1], row[2], str(q_t), str(row[3]), str(row[4]),
                 str(row[5]), str(row[6]), str(row[7]), str(row[8])]))
            t_inventory += q_t * row[4]
            self.win.t_inventary.setText(
                locale.toCurrencyString(t_inventory))
            i += 1
        self.win.tree.addTopLevelItems(item)
        i = 0
        for i in range(self.win.tree.topLevelItemCount()):
            self.win.tree.resizeColumnToContents(i)
            i += 1
        self.win.tree.setCurrentItem(self.win.tree.itemAt(0, 0))

    def update_list_sales(self):
        self.win.troo.clear()
        t_exit = 0
        locale = QtC.QLocale(QtC.QLocale.Spanish, QtC.QLocale.Chile)
        self.win.t_venta.setText(locale.toCurrencyString(t_exit))
        query = """select id, name, quantity, price from sales"""
        db_rows = database.run_query(query)
        item = []
        for row in db_rows:
            item.append(ui_inventary.QTreeWidgetItem(
                [row[1], str(row[2]), str(row[3])]))
            t_exit += row[2]*row[3]
            self.win.t_venta.setText(locale.toCurrencyString(t_exit))
        self.win.troo.addTopLevelItems(item)
        for i in range(self.win.troo.topLevelItemCount()):
            self.win.troo.resizeColumnToContents(i)
            i += 1

    def add_product_exit(self):
        self.win.l_info_exit.setText("")
        try:
            id_data = self.win.tree.selectedItems()[0]
        except IndexError:
            self.win.l_info_exit.setText("por favor seleccione un producto.")
        if self.win.c_local.currentIndex() == 0:
            cantidad = int(id_data.text(7))
        elif self.win.c_local.currentIndex() == 1:
            cantidad = int(id_data.text(8))
        else:
            cantidad = int(id_data.text(9))
        i_add = int(self.win.i_add.text())
        if not i_add.is_integer():
            self.win.l_info_exit.setText("Valor Incorrecto!")
        elif cantidad < i_add:
            self.win.l_info_exit.setText("No hay suficiente stock")
        elif cantidad >= i_add:
            try:
                query = """insert into sales (name, quantity, price)
                values (%s, %s, %s)"""
                name = id_data.text(2)
                price = int(id_data.text(6))
                parameters = (name, i_add, price)
                database.run_query_edit(query, parameters)
                self.win.l_info_exit.setText(f"Producto {name} fue agregado")
                self.update_list_sales()
            except database.maria.errors.IntegrityError as err:
                self.win.l_info_exit.setText(f"{err}")

    def delete_exit(self, id_data):
        """función eliminar de salida inventario"""
        self.win.l_info_exit.setText("")
        id_data = self.win.troo.selectedItems()
        try:
            id_data[0].text(0)
        except IndexError:
            self.win.l_info_exit.setText("por favor seleccione un producto")
            return
        self.win.l_info_exit.setText("")
        name = id_data[0].text(0)
        query = "DELETE FROM sales WHERE name = %s"
        database.run_query_edit(query, (name,))
        self.win.l_info_exit.setText(f"{name} fue eliminado correctamente")
        self.update_list_sales()

    def add_user(self):
        query = "insert into users (name, password) values (%s,%s)"
        user = QtW.QInputDialog.getText(
            None, "Inicializacion", "Introduzca nuevo usuario:")
        key = QtW.QInputDialog.getText(
            None, "Inicializacion", "contraseña:", QtW.QLineEdit.Password)
        parameters = (user, key)
        database.run_query_edit(query, parameters)

    def history(self):
        # self.hide()
        query = """select name, quantity, price, user, date from history"""
        db_rows = database.run_query(query)
        try:
            db_rows[0]
            self.win_h = History()
            self.win_h.show()
        except TypeError:
            self.win.l_info_exit.setText("Historial Vacio")

    def close_local(self):
        date = datetime.now()
        d_month = str(date.month)
        d_year = str(date.year)
        dir_history = "history/"+d_year+"/"+d_month
        if not os.path.exists(dir_history):
            os.makedirs(dir_history)

        if not os.path.exists(dir_history + "/" +
                              date.strftime("%d-%m-%Y %H:%M:%S")+".xlsx"):
            xl_save = Workbook()
            xl_active = xl_save.active
            query = """select id, name, price, quantity, user, action,
            date from history"""
            db_rows = database.run_query(query)
            for row in db_rows:
                xl_active.append(row)
                query_d = "DELETE FROM history WHERE name=%s"
                database.run_query_edit(query_d, (row[2],))
            xl_save.save(dir_history + "/" +
                         date.strftime("%d-%m-%Y %H:%M:%S")+".xlsx")


class History(ui_history.QMainWindow):
    def __init__(self):
        super().__init__()
        self.win_h = ui_history.Ui_history()
        self.win_h.setupUi(self)
        self.win_h.l_th.setText("0")
        self.update_list_history()

    def update_list_history(self):
        self.win_h.truu.clear()
        t_hist = 0
        locale = QtC.QLocale(QtC.QLocale.Spanish, QtC.QLocale.Chile)
        self.win_h.l_th.setText(locale.toCurrencyString(t_hist))
        query = """select name, quantity, price, user, action, date
        from history"""
        db_rows = database.run_query(query)
        item = []
        for row in db_rows:
            item.append(ui_inventary.QTreeWidgetItem(
                [row[0], str(row[2]), str(row[1]), str(row[3]), str(row[4]),
                 str(row[5])]))
            t_hist += row[2]*row[1]
            self.win_h.l_th.setText(locale.toCurrencyString(t_hist))
        self.win_h.truu.addTopLevelItems(item)
        for i in range(self.win_h.truu.topLevelItemCount()):
            self.win_h.truu.resizeColumnToContents(i)
            i += 1


class Edit(ui_edit.QDialog):
    def __init__(self, id_data):
        super().__init__()
        self.win_e = ui_edit.Ui_edit()
        self.win_e.setupUi(self)
        try:
            i_code = self.win_e.i_code.setText(id_data.text(1))
            i_name = self.win_e.i_name.setText(id_data.text(2))
            i_shop = self.win_e.i_shop.setText(id_data.text(4))
            i_gana = self.win_e.i_gana.setText(id_data.text(5))
            i_location = self.win_e.i_location.setText(id_data.text(7))
            i_location2 = self.win_e.i_location2.setText(id_data.text(8))
            i_location3 = self.win_e.i_location3.setText(id_data.text(9))
            self.win_e.buttonBox.accepted.connect(
                lambda: self.edit_records(i_code, i_name, i_shop, i_gana,
                                          i_location, i_location2, i_location3,
                                          id_data))
        except IndexError:
            QtW.QMessageBox.warning(None, "por favor seleccione un producto.")

    def edit_records(code, name, shop, gana, location, location2, location3,
                     id_data):
        query = """update product set code=%s, name=%s, price_buy=%s,
        ganancia=%s, price_sales=%s, location=%s , location2=%s, location3=%s
        where code=%s"""
        parameters = (code, name, shop, gana, location, location2, location3,
                      id_data.text(1))
        database.run_query_edit(query, parameters)
        history = Product()
        quantity = location+location2+location3
        if location != id_data.text(7) or location2 != id_data.text(8) or (
                location3 == id_data.text(9)):
            history.add_product_history(
                name, shop, quantity, history.user, f"""Producto {name}
                Modificado {location} a {id_data.text(7)}, {location2} a
                {id_data.text(8)}, {location2} a {id_data.text(9)}""")
        else:
            history.add_product_history(name, shop, quantity, history.user,
                                        f"Producto {name} Modificado")


def main():
    database.create_database()
    database.create_database_users()
    database.create_table()
    database.create_table_sales()
    database.create_database_history()
    app = ui_login.QApplication(sys.argv)
    login_app = Login()
    login_app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
