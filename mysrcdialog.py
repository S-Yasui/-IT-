# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mysrcdialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(410, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 25, 90, 16))
        self.label.setObjectName("label")
        self.srcText = QtWidgets.QLineEdit(Dialog)
        self.srcText.setGeometry(QtCore.QRect(130, 25, 230, 20))
        self.srcText.setObjectName("srcText")
        self.srcAllButton = QtWidgets.QPushButton(Dialog)
        self.srcAllButton.setGeometry(QtCore.QRect(130, 60, 75, 23))
        self.srcAllButton.setObjectName("srcAllButton")
        self.srcButton = QtWidgets.QPushButton(Dialog)
        self.srcButton.setGeometry(QtCore.QRect(220, 60, 75, 23))
        self.srcButton.setObjectName("srcButton")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(310, 60, 75, 23))
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(Dialog)
        self.srcAllButton.clicked.connect(Dialog.searchAll)
        self.srcButton.clicked.connect(Dialog.search)
        self.cancelButton.clicked.connect(Dialog.close)
        self.srcText.returnPressed.connect(Dialog.search)
        self.srcText.textChanged['QString'].connect(Dialog.resetSearchIndex)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "検索する文字列"))
        self.srcAllButton.setText(_translate("Dialog", "すべて検索"))
        self.srcButton.setText(_translate("Dialog", "次を検索"))
        self.cancelButton.setText(_translate("Dialog", "キャンセル"))

