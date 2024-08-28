# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'inventaryIiebyP.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_inventory(object):
    def setupUi(self, inventory):
        if not inventory.objectName():
            inventory.setObjectName(u"inventory")
        inventory.resize(1280, 740)
        font = QFont()
        font.setPointSize(10)
        inventory.setFont(font)
        self.action_c = QAction(inventory)
        self.action_c.setObjectName(u"action_c")
        self.action_u = QAction(inventory)
        self.action_u.setObjectName(u"action_u")
        self.action_h = QAction(inventory)
        self.action_h.setObjectName(u"action_h")
        self.action_i = QAction(inventory)
        self.action_i.setObjectName(u"action_i")
        self.action_e = QAction(inventory)
        self.action_e.setObjectName(u"action_e")
        self.action_s = QAction(inventory)
        self.action_s.setObjectName(u"action_s")
        self.centralwidget = QWidget(inventory)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setFont(font)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 1280, 720))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.tree = QTreeWidget(self.frame)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(9, Qt.AlignCenter);
        __qtreewidgetitem.setFont(9, font);
        __qtreewidgetitem.setTextAlignment(8, Qt.AlignCenter);
        __qtreewidgetitem.setFont(8, font);
        __qtreewidgetitem.setTextAlignment(7, Qt.AlignCenter);
        __qtreewidgetitem.setFont(7, font);
        __qtreewidgetitem.setTextAlignment(6, Qt.AlignCenter);
        __qtreewidgetitem.setFont(6, font);
        __qtreewidgetitem.setTextAlignment(5, Qt.AlignCenter);
        __qtreewidgetitem.setFont(5, font);
        __qtreewidgetitem.setTextAlignment(4, Qt.AlignCenter);
        __qtreewidgetitem.setFont(4, font);
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setFont(3, font);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setFont(2, font);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setFont(1, font);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font);
        self.tree.setHeaderItem(__qtreewidgetitem)
        self.tree.setObjectName(u"tree")
        self.tree.setGeometry(QRect(0, 90, 884, 533))
        self.tree.setFont(font)
        self.tree.setStyleSheet(u"")
        self.tree.header().setMinimumSectionSize(20)
        self.tree.header().setDefaultSectionSize(87)
        self.b_up = QPushButton(self.frame)
        self.b_up.setObjectName(u"b_up")
        self.b_up.setGeometry(QRect(1020, 40, 141, 36))
        self.b_up.setBaseSize(QSize(0, 0))
        self.b_up.setFont(font)
        self.troo = QTreeWidget(self.frame)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem1.setFont(2, font);
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem1.setFont(1, font);
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem1.setFont(0, font);
        self.troo.setHeaderItem(__qtreewidgetitem1)
        self.troo.setObjectName(u"troo")
        self.troo.setGeometry(QRect(910, 90, 371, 291))
        self.b_add = QPushButton(self.frame)
        self.b_add.setObjectName(u"b_add")
        self.b_add.setGeometry(QRect(1050, 380, 71, 31))
        self.b_del = QPushButton(self.frame)
        self.b_del.setObjectName(u"b_del")
        self.b_del.setGeometry(QRect(980, 380, 71, 31))
        self.b_fin = QPushButton(self.frame)
        self.b_fin.setObjectName(u"b_fin")
        self.b_fin.setGeometry(QRect(910, 380, 71, 31))
        self.i_add = QLineEdit(self.frame)
        self.i_add.setObjectName(u"i_add")
        self.i_add.setGeometry(QRect(1120, 380, 51, 31))
        self.i_add.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.c_local = QComboBox(self.frame)
        self.c_local.addItem("")
        self.c_local.addItem("")
        self.c_local.addItem("")
        self.c_local.setObjectName(u"c_local")
        self.c_local.setGeometry(QRect(1170, 380, 108, 33))
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(940, 490, 87, 19))
        self.t_venta = QLabel(self.frame)
        self.t_venta.setObjectName(u"t_venta")
        self.t_venta.setGeometry(QRect(1020, 490, 101, 19))
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(320, 630, 151, 19))
        self.t_inventary = QLabel(self.frame)
        self.t_inventary.setObjectName(u"t_inventary")
        self.t_inventary.setGeometry(QRect(470, 630, 87, 19))
        self.b_edit = QPushButton(self.frame)
        self.b_edit.setObjectName(u"b_edit")
        self.b_edit.setGeometry(QRect(0, 620, 114, 36))
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 670, 111, 19))
        self.i_fcode = QLineEdit(self.frame)
        self.i_fcode.setObjectName(u"i_fcode")
        self.i_fcode.setGeometry(QRect(120, 660, 113, 33))
        self.i_fcode.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(260, 670, 151, 19))
        self.i_fdesc = QLineEdit(self.frame)
        self.i_fdesc.setObjectName(u"i_fdesc")
        self.i_fdesc.setGeometry(QRect(410, 660, 113, 33))
        self.i_fdesc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.i_fdesc2 = QLineEdit(self.frame)
        self.i_fdesc2.setObjectName(u"i_fdesc2")
        self.i_fdesc2.setGeometry(QRect(530, 660, 113, 33))
        self.i_fdesc2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.l_info_exit = QLabel(self.frame)
        self.l_info_exit.setObjectName(u"l_info_exit")
        self.l_info_exit.setGeometry(QRect(906, 438, 361, 51))
        self.b_his = QPushButton(self.frame)
        self.b_his.setObjectName(u"b_his")
        self.b_his.setGeometry(QRect(1020, 600, 114, 36))
        self.b_delete = QPushButton(self.frame)
        self.b_delete.setObjectName(u"b_delete")
        self.b_delete.setGeometry(QRect(120, 620, 114, 36))
        inventory.setCentralWidget(self.centralwidget)
        self.menu = QMenuBar(inventory)
        self.menu.setObjectName(u"menu")
        self.menu.setGeometry(QRect(0, 0, 1280, 28))
        self.menu.setDefaultUp(False)
        self.menuUsuario = QMenu(self.menu)
        self.menuUsuario.setObjectName(u"menuUsuario")
        self.menu2 = QMenu(self.menu)
        self.menu2.setObjectName(u"menu2")
        inventory.setMenuBar(self.menu)

        self.menu.addAction(self.menuUsuario.menuAction())
        self.menu.addAction(self.menu2.menuAction())
        self.menuUsuario.addAction(self.action_c)
        self.menuUsuario.addSeparator()
        self.menuUsuario.addAction(self.action_u)
        self.menu2.addAction(self.action_h)
        self.menu2.addAction(self.action_i)
        self.menu2.addAction(self.action_e)
        self.menu2.addSeparator()
        self.menu2.addAction(self.action_s)

        self.retranslateUi(inventory)

        QMetaObject.connectSlotsByName(inventory)
    # setupUi

    def retranslateUi(self, inventory):
        inventory.setWindowTitle(QCoreApplication.translate("inventory", u"OIQ Inventary", None))
        self.action_c.setText(QCoreApplication.translate("inventory", u"&Cierre Local", None))
        self.action_u.setText(QCoreApplication.translate("inventory", u"&Usuarios", None))
        self.action_h.setText(QCoreApplication.translate("inventory", u"&Abrir Historial", None))
        self.action_i.setText(QCoreApplication.translate("inventory", u"&Importar CVS", None))
        self.action_e.setText(QCoreApplication.translate("inventory", u"&Exportar CVS", None))
        self.action_s.setText(QCoreApplication.translate("inventory", u"&Cerrar Sesi\u00f3n", None))
        ___qtreewidgetitem = self.tree.headerItem()
        ___qtreewidgetitem.setText(9, QCoreApplication.translate("inventory", u"LOCAL", None));
        ___qtreewidgetitem.setText(8, QCoreApplication.translate("inventory", u"BODEGA", None));
        ___qtreewidgetitem.setText(7, QCoreApplication.translate("inventory", u"RENDIC", None));
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("inventory", u"VENTA", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("inventory", u"GANANCIA", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("inventory", u"COMPRA", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("inventory", u"CANT.", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("inventory", u"DESCRIPCION", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("inventory", u"CODIGO", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("inventory", u"ITEM", None));
        self.b_up.setText(QCoreApplication.translate("inventory", u"Atualizar Lista", None))
        ___qtreewidgetitem1 = self.troo.headerItem()
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("inventory", u"Precio", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("inventory", u"Cantidad", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("inventory", u"Descripcion", None));
        self.b_add.setText(QCoreApplication.translate("inventory", u"Agregar", None))
        self.b_del.setText(QCoreApplication.translate("inventory", u"Eliminar", None))
        self.b_fin.setText(QCoreApplication.translate("inventory", u"Retirar", None))
        self.i_add.setInputMask("")
        self.i_add.setText(QCoreApplication.translate("inventory", u"1", None))
        self.c_local.setItemText(0, QCoreApplication.translate("inventory", u"Rendic", None))
        self.c_local.setItemText(1, QCoreApplication.translate("inventory", u"Bodega", None))
        self.c_local.setItemText(2, QCoreApplication.translate("inventory", u"Local", None))

        self.label_2.setText(QCoreApplication.translate("inventory", u"Total:", None))
        self.t_venta.setText(QCoreApplication.translate("inventory", u"0", None))
        self.label.setText(QCoreApplication.translate("inventory", u"Total inventario:", None))
        self.t_inventary.setText(QCoreApplication.translate("inventory", u"0", None))
        self.b_edit.setText(QCoreApplication.translate("inventory", u"Editar", None))
        self.label_3.setText(QCoreApplication.translate("inventory", u"Filtro Codigo:", None))
        self.label_4.setText(QCoreApplication.translate("inventory", u"Filtro Descripcion:", None))
        self.l_info_exit.setText("")
        self.b_his.setText(QCoreApplication.translate("inventory", u"Historial", None))
        self.b_delete.setText(QCoreApplication.translate("inventory", u"Eliminar", None))
        self.menuUsuario.setTitle(QCoreApplication.translate("inventory", u"&Usuario", None))
        self.menu2.setTitle(QCoreApplication.translate("inventory", u"Arc&hivo", None))
    # retranslateUi

