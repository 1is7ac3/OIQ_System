import sys
import ui_login
import database
import main
import tkinter as tk


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
            print(self.ui.i_user.currentText())
            if self.ui.i_user.currentText() == name:
                if self.ui.i_key.text() == self.key_box[i]:
                    login_app.close()
                    window = tk.Tk()
                    screen_width = window.winfo_screenwidth()
                    screen_height = window.winfo_screenheight()
                    window.geometry(f"{screen_width}x{screen_height}")
                    main.Product(window, self.ui.i_user.currentText(), 0)
                    window.mainloop()
                else:
                    self.ui.key_result.setText("contraseña incorrecta")
                    break
            i += 1


if __name__ == "__main__":
    app = ui_login.QApplication(sys.argv)
    login_app = MiApp()
    login_app.show()
    sys.exit(app.exec())
