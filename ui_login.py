# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginrxqtHP.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QWidget)

class Ui_sesion(object):
    def setupUi(self, sesion):
        if not sesion.objectName():
            sesion.setObjectName(u"sesion")
        sesion.resize(635, 480)
        font = QFont()
        font.setFamilies([u"C059 [urw]"])
        sesion.setFont(font)
        icon = QIcon()
        icon.addFile(u"inventary.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        sesion.setWindowIcon(icon)
        self.centralwidget = QWidget(sesion)
        self.centralwidget.setObjectName(u"centralwidget")
        font1 = QFont()
        font1.setFamilies([u"C059 [urw]"])
        font1.setPointSize(14)
        self.centralwidget.setFont(font1)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        self.frame.setStyleSheet(u"background: rgb(41, 45, 50);\n"
"border-radius: 20px;\n"
"border: 1px;\n"
"")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.l_user = QLabel(self.frame)
        self.l_user.setObjectName(u"l_user")
        self.l_user.setGeometry(QRect(250, 110, 141, 31))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(False)
        self.l_user.setFont(font2)
        self.l_user.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.l_user.setTextFormat(Qt.TextFormat.PlainText)
        self.l_user.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.l_key = QLabel(self.frame)
        self.l_key.setObjectName(u"l_key")
        self.l_key.setGeometry(QRect(260, 220, 131, 41))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_key.sizePolicy().hasHeightForWidth())
        self.l_key.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setFamilies([u"Hack Nerd Font"])
        font3.setPointSize(14)
        font3.setBold(False)
        self.l_key.setFont(font3)
        self.l_key.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.l_key.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.i_user = QComboBox(self.frame)
        self.i_user.setObjectName(u"i_user")
        self.i_user.setGeometry(QRect(220, 150, 201, 41))
        self.i_user.setFont(font2)
        self.i_user.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.i_user.setAutoFillBackground(False)
        self.i_user.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-radius: 20px;")
        self.i_user.setEditable(False)
        self.b_start = QPushButton(self.frame)
        self.b_start.setObjectName(u"b_start")
        self.b_start.setGeometry(QRect(70, 400, 171, 41))
        self.b_start.setFont(font2)
        self.b_start.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.b_start.setAutoFillBackground(False)
        self.b_start.setStyleSheet(u"QPushButton{\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"	color: rgb(0, 170, 0);\n"
"}\n"
"")
        self.b_exit = QPushButton(self.frame)
        self.b_exit.setObjectName(u"b_exit")
        self.b_exit.setGeometry(QRect(480, 400, 114, 36))
        self.b_exit.setMouseTracking(True)
        self.b_exit.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.b_exit.setStyleSheet(u"QPushButton{\n"
"	color: rgb(255, 255, 255)\n"
"}\n"
"QPushButton:hover{\n"
"	color: rgb(255, 0, 0);\n"
"}")
        self.b_exit.setCheckable(False)
        self.b_exit.setAutoDefault(False)
        self.i_key = QLineEdit(self.frame)
        self.i_key.setObjectName(u"i_key")
        self.i_key.setGeometry(QRect(200, 260, 251, 41))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.i_key.sizePolicy().hasHeightForWidth())
        self.i_key.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setPointSize(13)
        font4.setBold(False)
        self.i_key.setFont(font4)
        self.i_key.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.i_key.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.i_key.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.i_key.setAutoFillBackground(False)
        self.i_key.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-radius: 20px;")
        self.i_key.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_result = QLabel(self.frame)
        self.user_result.setObjectName(u"user_result")
        self.user_result.setGeometry(QRect(220, 200, 211, 20))
        self.user_result.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.key_result = QLabel(self.frame)
        self.key_result.setObjectName(u"key_result")
        self.key_result.setGeometry(QRect(0, 320, 631, 41))
        self.key_result.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 0, 0);")
        self.key_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.l_user.raise_()
        self.l_key.raise_()
        self.i_user.raise_()
        self.i_key.raise_()
        self.user_result.raise_()
        self.key_result.raise_()
        self.b_start.raise_()
        self.b_exit.raise_()

        self.horizontalLayout.addWidget(self.frame)

        sesion.setCentralWidget(self.centralwidget)
#if QT_CONFIG(shortcut)
        self.user_result.setBuddy(self.i_key)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.i_user, self.i_key)
        QWidget.setTabOrder(self.i_key, self.b_exit)
        QWidget.setTabOrder(self.b_exit, self.b_start)

        self.retranslateUi(sesion)
        self.b_exit.clicked.connect(sesion.close)
        self.i_key.cursorPositionChanged.connect(self.i_key.setFocus)

        QMetaObject.connectSlotsByName(sesion)
    # setupUi

    def retranslateUi(self, sesion):
        sesion.setWindowTitle(QCoreApplication.translate("sesion", u"Inicio de sesi\u00f3n", None))
        self.l_user.setText(QCoreApplication.translate("sesion", u"Usuario", None))
        self.l_key.setText(QCoreApplication.translate("sesion", u"Contrase\u00f1a", None))
        self.b_start.setText(QCoreApplication.translate("sesion", u"Iniciar Sesi\u00f3n", None))
        self.b_exit.setText(QCoreApplication.translate("sesion", u"Salir", None))
        self.i_key.setPlaceholderText(QCoreApplication.translate("sesion", u"Ingrese Contrase\u00f1a", None))
        self.user_result.setText("")
        self.key_result.setText(QCoreApplication.translate("sesion", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
    # retranslateUi

