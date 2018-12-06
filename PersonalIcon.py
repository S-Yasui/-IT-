# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore as Qc, QtGui as Qg, QtWidgets as Qw    #（補足1）
from PyQt5.QtCore import Qt
import myicon

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage

class PersonalIcon(Qw.QWidget):

    #----------------------------------------------
    # （内部処理）初期化処理
    #----------------------------------------------
    def __init__(self, parent, imgSize, image=None, text=None):  #クラスの初期化

        super().__init__(parent)            #上位クラスの初期化ルーチンを呼び出す（補足2）
        self.ui = myicon.Ui_Form()
        self.ui.setupUi(self)

        pixmap = QPixmap(image)
        self.ui.imgField.setPixmap(pixmap.scaled(imgSize, imgSize, aspectRatioMode=Qt.KeepAspectRatio))
        self.ui.textField.setText(text)

    #----------------------------------------------
    # （内部処理）画像設定
    #----------------------------------------------
    def setImage(self, image, imgSize):
         pixmap = QPixmap(image)
         self.ui.imgField.setPixmap(pixmap.scaled(imgSize, imgSize, aspectRatioMode=Qt.KeepAspectRatio))

    #----------------------------------------------
    # （内部処理）テキスト設定
    #----------------------------------------------
    def setText(self, text):
        self.ui.textField.setText(text)
