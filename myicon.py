# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myicon.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(70, 50)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textField = QtWidgets.QLabel(Form)
        self.textField.setMinimumSize(QtCore.QSize(0, 20))
        self.textField.setText("")
        self.textField.setAlignment(QtCore.Qt.AlignCenter)
        self.textField.setObjectName("textField")
        self.verticalLayout.addWidget(self.textField)
        self.imgField = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imgField.sizePolicy().hasHeightForWidth())
        self.imgField.setSizePolicy(sizePolicy)
        self.imgField.setText("")
        self.imgField.setAlignment(QtCore.Qt.AlignCenter)
        self.imgField.setObjectName("imgField")
        self.verticalLayout.addWidget(self.imgField)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

