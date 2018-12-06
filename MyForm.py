# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore as Qc, QtGui as Qg, QtWidgets as Qw    #（補足1）
from PyQt5.QtWidgets import QFileDialog
import os
from ctypes import *
user32 = windll.user32 #デバッグ用

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtCore
from PersonalIcon import PersonalIcon
from MyFaceApi import *
from MyCosmosDB import *
import json
import io
import configparser
import const

import Sample as Sample               #デザイナーで作った画面をインポートする


class MyForm(Qw.QMainWindow):               #MyFormという名前でQMainWindowのサブクラス作成

    # クラス変数
    gDeskStatusList = {}        # 座席状態リスト

    #----------------------------------------------
    # （内部処理）初期化処理
    #----------------------------------------------
    def __init__(self, parent=None):        #クラスの初期化

        super().__init__(parent)            #上位クラスの初期化ルーチンを呼び出す（補足2）
        self.ui = Sample.Ui_MainWindow()     #先ほど作ったhello.pyの中にあるクラスの
        self.ui.setupUi(self)               #このコマンドを実行する

        # 終了処理用
        self.setAttribute(Qc.Qt.WA_DeleteOnClose, True)
        self.destroyed.connect(MyForm._on_destroyed)

        # ウィンドウタイトル
        self.setWindowTitle('Sample')

        # 背景設定（背景もDBから情報を取得できれば一番良い）
        pixmap = QPixmap('desk_office.jpg')
        self.ui.img_main.setPixmap(pixmap.scaled(self.ui.img_main.width(),self.ui.img_main.height(),Qc.Qt.KeepAspectRatio))
        pixmap = QPixmap('desk_satellite.jpg')
        self.ui.img_satellite.setPixmap(pixmap.scaled(self.ui.img_satellite.width(),self.ui.img_satellite.height(),Qc.Qt.KeepAspectRatio))
        pixmap = QPixmap('desk_telework.jpg')
        self.ui.img_telework.setPixmap(pixmap.scaled(self.ui.img_telework.width(),self.ui.img_telework.height(),Qc.Qt.KeepAspectRatio))

        self.setFixedSize(1200, 900)

        # クラス変数初期化
        global gDeskStatusList
        gDeskStatusList = {}

        # 設定ファイル読込
        self.getSettings()

        # 初期表示
        self.getList()


    #----------------------------------------------
    # （内部処理）設定ファイル読込処理
    #----------------------------------------------
    def getSettings(self):

        inifile = configparser.ConfigParser()
        with io.open('./config.ini', 'r', encoding='utf_8_sig') as fp:
            inifile.readfp(fp)

        const.DESK_ID = inifile.get('settings', 'deskId')
        const.FLOOR_ID = inifile.get('settings', 'floorId')


    #----------------------------------------------
    # （イベント）更新ボタン
    #----------------------------------------------
    def updateScr(self):

        # アイコン更新処理呼び出し
        self.updateIcon()

    #----------------------------------------------
    # （内部処理）アイコン更新
    #----------------------------------------------
    def updateIcon(self):

        global gDeskStatusList

        # 人物情報を取得
        result = MyFaceApi.getPersonInfo()

        # 更新情報を初期化
        deskId = const.DESK_ID        # 設定ファイルの値
        floorId = const.FLOOR_ID      # 設定ファイルの値
        userId = ''
        userName = ''
        statusCd = ''

        if result == None:
            pass
        elif len(result)==0:
            # 席に誰もいない
            deskInfo = gDeskStatusList[deskId]
            userId = deskInfo['user_id']
            userName = deskInfo['user_name']
            if not userId == None:
                if len(userId)>0:
                    statusCd = '4'
        else:
            #　誰か座っている
            personInfo = result[0]
            userId = personInfo['userId']
            userName = personInfo['userName']
            statusCd = '1'

        # DB情報を更新
        MyCosmosDB.updateDeskStatus(deskId, floorId, userId, userName, statusCd)

        # 表示情報を更新
        self.getList()


    #----------------------------------------------
    # （内部処理）リスト取得
    #----------------------------------------------
    def getList(self):

        deskStatusTable = MyCosmosDB.getDeskStatusTable(const.FLOOR_ID)
        statusIconList = {'1':'icon\icon_image_01.png', '2':'icon\icon_image_02.png', '3':'icon\icon_image_03.png', '4':'icon\icon_image_04.png'}

        global gDeskStatusList
        updateFlg = False
        if len(gDeskStatusList)>0:
            updateFlg = True

        for desk in deskStatusTable:

            user_id = None
            user_name = None
            img_path = None

            if len(desk['userId']) > 0:
                user_id = desk['userId']

            if len(desk['userName']) > 0:
                user_name = desk['userName']

            if len(desk['statusCd']) > 0:
                img_path = statusIconList[desk['statusCd']]

            if updateFlg:
                # 座席状態リスト作成済の場合
                deskInfo = gDeskStatusList[desk['RowKey']]
                deskInfo['icon'].setImage(img_path, 20)
                deskInfo['icon'].setText(user_name)
                deskInfo['user_id'] = user_id
                deskInfo['user_name'] = user_name
            else:
                #　座席状態リスト未作成の場合
                img_icon = PersonalIcon(self.ui.img_main, 20, img_path, user_name)
                img_icon.setGeometry(desk['x'], desk['y'], img_icon.width(), img_icon.height())
                gDeskStatusList.update({desk['RowKey']:{'user_id':user_id, 'user_name':user_name, 'icon':img_icon, 'x':desk['x'], 'y':desk['y']}})


    #----------------------------------------------
    # （内部処理）終了処理
    #----------------------------------------------
    def _on_destroyed():

        # DB情報を初期化
        userId = ''
        userName = ''
        statusCd = ''
        MyCosmosDB.updateDeskStatus(const.DESK_ID, const.FLOOR_ID, userId, userName, statusCd)

        # 一時保存写真を削除
        if os.path.exists('image\image.png'):
            os.remove('image\image.png')


if __name__ == '__main__':

    app = Qw.QApplication(sys.argv)         #パラメータは正しくはコマンドライン引数を与える
    wmain = MyForm()                        #MyFormのインスタンスを作って
    wmain.show()                            #表示する
    sys.exit(app.exec())                    #こうやって終了コードを渡して抜けるのが礼儀
