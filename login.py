import sys
import ui_login
import ui_inventary
import database
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC


class MiApp(ui_login.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui_login.Ui_sesion()
        self.ui.setupUi(self)
        # eliminar barra
        self.setWindowFlag(ui_login.Qt.FramelessWindowHint)
        # transparente
        self.setAttribute(ui_login.Qt.WA_TranslucentBackground)
        self.ui.b_start.clicked.connect(self.sesion)
        query = "select id, name, password from users"
        db_rows = database.run_query_mariadb(query)
        self.users_box = ["admin"]
        self.key_box = ["admin"]
        for row in db_rows:
            self.users_box.append(row[1])
            self.key_box.append(row[2])
        self.ui.i_user.addItems(self.users_box)
        self.ui.i_user.setCurrentIndex(0)
        self.ui.i_key.setFocus()
        self.ui.i_key.setEchoMode(ui_login.QLineEdit.Password)

    def sesion(self):
        self.ui.key_result.setText("")
        i = 0
        for name in self.users_box:
            if self.ui.i_user.currentText() == name:
                if self.ui.i_key.text() == self.key_box[i]:
                    self.hide()
                    self.window = product()
                    self.window.show()
                else:
                    self.ui.key_result.setText("contraseña incorrecta")
                    break
            i += 1


class product(ui_inventary.QMainWindow):
    def __init__(self):
        super().__init__()
        self.win = ui_inventary.Ui_inventory()
        self.win.setupUi(self)
        self.win.action_i.triggered.connect(self.import_lote)
        self.win.action_e.triggered.connect(self.export_lote)
        self.win.action_s.triggered.connect(self.close)
        self.win.action_u.triggered.connect(self.add_user)
        self.win.b_up.clicked.connect(self.update_list)
        self.win.b_add.clicked.connect(self.add_product_exit)
        self.win.b_del.clicked.connect(self.delete_exit)
        self.win.b_fin.clicked.connect(self.charge)
        self.update_list()
        self.update_list_sales()
        self.win.i_fcode.textChanged.connect(self.search_code)
        self.win.i_fdesc.textChanged.connect(self.search_desc)
        self.win.i_fdesc2.textChanged.connect(self.search_desc)

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
        db_rows = database.run_query_mariadb(qdata)
        for row in db_rows:
            qdata2 = """select name, quantity from sales"""
            db_rows2 = database.run_query_mariadb(qdata2)
            for row2 in db_rows2:
                if row2[0] == row[0]:
                    new_qua = row[1]-row2[1]
                    if new_qua >= 0:
                        query = f"""UPDATE product SET
                                        {ubica}=%s WHERE name=%s"""
                        parameters = (new_qua, row2[0])
                        database.run_query_mariadb_edit(query, parameters)
                        query2 = "DELETE FROM sales WHERE name=%s"
                        database.run_query_mariadb_edit(query2, (row2[0],))
        self.update_list()
        self.update_list_sales()

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

    def update_list(self):
        self.win.tree.clear()
        t_inventory = 0
        locale = QtC.QLocale(QtC.QLocale.Spanish, QtC.QLocale.Chile)
        self.win.t_inventary.setText(
            locale.toCurrencyString(t_inventory))
        query = """select id, code, name, price_buy, ganancia, price_sales,
            location, location2, location3 from product order by name ASC"""
        db_rows = database.run_query_mariadb(query)
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
        db_rows = database.run_query_mariadb(query)
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
                database.run_query_mariadb_edit(query, parameters)
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
        database.run_query_mariadb_edit(query, (name,))
        self.win.l_info_exit.setText(f"{name} fue eliminado correctamente")
        self.update_list_sales()

    def add_user():
        pass


def main():
    database.create_database_mariadb()
    database.create_database_users()
    database.create_table_mariadb()
    database.create_table_sales_mariadb()
    database.create_database_history()
    app = ui_login.QApplication(sys.argv)
    login_app = MiApp()
    login_app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
