# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edityXSyud.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(409, 489)
        self.buttonBox = QDialogButtonBox(edit)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 400, 411, 31))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)
        self.formLayoutWidget = QWidget(edit)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(30, 30, 341, 341))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formLayout.setHorizontalSpacing(0)
        self.formLayout.setVerticalSpacing(16)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.i_code = QLineEdit(self.formLayoutWidget)
        self.i_code.setObjectName(u"i_code")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.i_code)

        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.i_name = QLineEdit(self.formLayoutWidget)
        self.i_name.setObjectName(u"i_name")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.i_name)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.i_shop = QLineEdit(self.formLayoutWidget)
        self.i_shop.setObjectName(u"i_shop")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.i_shop)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.i_gana = QLineEdit(self.formLayoutWidget)
        self.i_gana.setObjectName(u"i_gana")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.i_gana)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.i_location = QLineEdit(self.formLayoutWidget)
        self.i_location.setObjectName(u"i_location")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.i_location)

        self.label_6 = QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.i_location2 = QLineEdit(self.formLayoutWidget)
        self.i_location2.setObjectName(u"i_location2")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.i_location2)

        self.label_7 = QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.i_location3 = QLineEdit(self.formLayoutWidget)
        self.i_location3.setObjectName(u"i_location3")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.i_location3)


        self.retranslateUi(edit)
        self.buttonBox.accepted.connect(edit.accept)
        self.buttonBox.rejected.connect(edit.reject)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Editar", None))
        self.label_2.setText(QCoreApplication.translate("edit", u"Code:", None))
        self.label.setText(QCoreApplication.translate("edit", u"Nombre:", None))
        self.label_3.setText(QCoreApplication.translate("edit", u"Compra:", None))
        self.label_4.setText(QCoreApplication.translate("edit", u"Ganancia:", None))
        self.label_5.setText(QCoreApplication.translate("edit", u"Rendic:", None))
        self.label_6.setText(QCoreApplication.translate("edit", u"Bodega:", None))
        self.label_7.setText(QCoreApplication.translate("edit", u"Local:", None))
    # retranslateUi

