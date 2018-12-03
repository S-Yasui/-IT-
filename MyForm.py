# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore as Qc, QtGui as Qg, QtWidgets as Qw    #（補足1）
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import os.path

from ctypes import *
user32 = windll.user32 #デバッグ用

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PersonalIcon import PersonalIcon
from MyFaceApi import *
import json

import Sample as Sample               #デザイナーで作った画面をインポートする

class MyForm(Qw.QMainWindow):               #MyFormという名前でQMainWindowのサブクラス作成

    #グローバル変数
    gCurrentDir = ''            # カレントディレクトリ
    gImgIconList = {}           # アイコンリスト

    #----------------------------------------------
    # （内部処理）初期化処理
    #----------------------------------------------
    def __init__(self, parent=None):        #クラスの初期化

        super().__init__(parent)            #上位クラスの初期化ルーチンを呼び出す（補足2）
        self.ui = Sample.Ui_MainWindow()     #先ほど作ったhello.pyの中にあるクラスの
        self.ui.setupUi(self)               #このコマンドを実行する

        self.setWindowTitle('Sample')

        #背景設定（背景もDBから情報を取得できれば一番良い
        pixmap = QPixmap('desk.jpg')
        self.ui.img_main.setPixmap(pixmap)
        self.resize(pixmap.width()+100, pixmap.height()+100)
        self.setFixedSize(pixmap.width()+100, pixmap.height()+100)

        #グローバル変数初期化
        global gCurrentDir
        gCurrentDir = ''
        global gImgIconList
        gImgIconList = {}

        gImgIconList = self.getList()

    #----------------------------------------------
    # （イベント）更新ボタン
    #----------------------------------------------
    def openFile(self):

        # アイコン更新処理呼び出し
        self.updateIcon()

    #----------------------------------------------
    # （内部処理）アイコン更新
    #----------------------------------------------
    def updateIcon(self):

        global gImgIconList

        # 人物情報を取得
        result = MyFaceApi.getPersonInfo()

        #これ以降はあとで取得した情報によってDB情報を更新する処理に変える

        for zasekiId, img_icon_info in gImgIconList.items():
            if zasekiId == '0000005':
                #とりあえず顔検出できたら5卓のアイコンを変えてみる
                if result == None:
                    #検知エラー
                    img_icon_info['icon'].setImage(None)
                    img_icon_info['icon'].setText(None)
                elif len(result) > 0:
                    personInfo = result[0]
                    img_icon_info['icon'].setImage('icon\icon_image_01.png')
                    img_icon_info['icon'].setText(personInfo['userName'])
                    img_icon_info['user_id'] = personInfo['userId']
                    img_icon_info['user_name'] = personInfo['userName']
                else:
                    img_icon_info['icon'].setImage('icon\icon_image_04.png')
                    #img_icon_info['icon'].setText(None)

            else:
               pass

        print(gImgIconList)


    #----------------------------------------------
    # （内部処理）リスト取得
    #----------------------------------------------
    def getList(self):

        # あとでDB情報を取得してリスト化する処理に変える

        #とりあえず適当に8人分くらいべた書き
        retList = {}

        for num in range(1, 9):
            zasekiId = format(num, '07x')
            if num <= 4:
                x = 170
                y = 90 + (90 * num)
            else:
                x = 260
                y = 90 + (90 * (num - 4))

            if num % 2 == 0:
                image_path = 'icon\icon_image_01.png'
                icon_text = 'ユーザ{0}'.format(num)
                user_id = 'S{0}'.format(format(num, '04x'))
            else:
                # 奇数ユーザはいない設定にしておく
                image_path = None
                icon_text = None
                user_id = None

            img_icon = PersonalIcon(self, image_path, icon_text)
            img_icon.setGeometry(x, y, img_icon.width(), img_icon.height())
            retList.update({zasekiId:{'user_id':user_id, 'user_name':icon_text, 'icon':img_icon, 'x':x, 'y':y}})

        return retList



if __name__ == '__main__':

    app = Qw.QApplication(sys.argv)         #パラメータは正しくはコマンドライン引数を与える
    wmain = MyForm()                        #MyFormのインスタンスを作って
    wmain.show()                            #表示する
    sys.exit(app.exec())                    #こうやって終了コードを渡して抜けるのが礼儀
