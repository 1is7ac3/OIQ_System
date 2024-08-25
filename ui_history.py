# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'historyIJdOfg.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_history(object):
    def setupUi(self, history):
        if not history.objectName():
            history.setObjectName(u"history")
        history.resize(1065, 391)
        self.centralwidget = QWidget(history)
        self.centralwidget.setObjectName(u"centralwidget")
        self.truu = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(5, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(4, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.truu.setHeaderItem(__qtreewidgetitem)
        self.truu.setObjectName(u"truu")
        self.truu.setGeometry(QRect(0, 10, 1071, 331))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 350, 131, 31))
        self.l_th = QLabel(self.centralwidget)
        self.l_th.setObjectName(u"l_th")
        self.l_th.setGeometry(QRect(160, 350, 101, 31))
        history.setCentralWidget(self.centralwidget)

        self.retranslateUi(history)

        QMetaObject.connectSlotsByName(history)
    # setupUi

    def retranslateUi(self, history):
        history.setWindowTitle(QCoreApplication.translate("history", u"Historial de ventas", None))
        ___qtreewidgetitem = self.truu.headerItem()
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("history", u"Fecha", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("history", u"Accion", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("history", u"Usuario", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("history", u"Cantidad", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("history", u"Precio", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("history", u"Producto", None));
        self.label.setText(QCoreApplication.translate("history", u"Total Ventas:", None))
        self.l_th.setText(QCoreApplication.translate("history", u"0", None))
    # retranslateUi

