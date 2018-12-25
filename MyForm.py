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
from MySearchDialog import *
from MyAudio import *
import json
import io
import configparser
import const
import time
#import concurrent.futures
import threading
from datetime import datetime


import Sample as Sample               #デザイナーで作った画面をインポートする


class MyForm(Qw.QMainWindow):               #MyFormという名前でQMainWindowのサブクラス作成

    # クラス変数
    gDeskStatusList = {}        # 座席状態リスト
    gIsSpeakingFlg = False      # 話し中フラグ
    gScrLock = threading.Lock()    # 画面ロック

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
        global gIsSpeakingFlg
        gIsSpeakingFlg = False
        global gScrLock
        gScrLock = threading.Lock()

        # 設定ファイル読込
        self.getSettings()

        # オフィス初期表示
        self.getMainList()


    #----------------------------------------------
    # （内部処理）設定ファイル読込処理
    #----------------------------------------------
    def getSettings(self):

        inifile = configparser.ConfigParser()
        with io.open('./config.ini', 'r', encoding='utf_8_sig') as fp:
            inifile.readfp(fp)

        const.DESK_ID = inifile.get('settings', 'deskId')
        const.FLOOR_ID = inifile.get('settings', 'floorId')
        const.FLOOR_ID_SAT = inifile.get('settings', 'floorIdSat')


    #----------------------------------------------
    # （イベント）検索ボタン
    #----------------------------------------------
    def search(self):

        # 画面情報が更新されるためロックする
        global gScrLock
        gScrLock.acquire()

        # 画面を最新化
        self.update()

        # メニューをロック
        self.ui.menubar.setEnabled(False)

        # 検索ボックス呼び出し
        global gDeskStatusList
        dlg = MySearchDialog(self, gDeskStatusList)
        dlg.show()
        dlg.exec_()

        # 検索結果をもとに戻す
        for deskInfo in gDeskStatusList.values():
            deskInfo['icon'].setOpacity(1.0)

        # メニューのロック解除
        self.ui.menubar.setEnabled(True)

        # 画面ロック解放前処理
        self.beforeReleaseScrLock()

        # 画面ロック解放
        gScrLock.release()


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
        global gIsSpeakingFlg

        # 人物情報を取得
        result = MyFaceApi.getPersonInfo()

        # 更新情報を初期化
        deskId = const.DESK_ID        # 設定ファイルの値
        userId = ''
        userName = ''
        statusCd = ''

        if result == None:
            pass
        elif len(result)==0:
            # 席に誰もいない
            if not len(gDeskStatusList)==0:
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
            if gIsSpeakingFlg:
                # 話し中
                statusCd = '2'
            else:
                statusCd = '1'

        # DB情報を更新
        MyCosmosDB.updateDeskStatus(deskId, userId, userName, statusCd)

        # オフィスの表示情報を更新
        self.getMainList()
        self.ui.statusbar.showMessage('更新しました。（{0}）'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))


    #----------------------------------------------
    # （内部処理）オフィス情報取得
    #----------------------------------------------
    def getMainList(self):

        # 画面情報が更新されるためロックする
        global gScrLock
        gScrLock.acquire()

        deskStatusTable = MyCosmosDB.getDeskStatusTable(const.FLOOR_ID, const.FLOOR_ID_SAT)
        statusIconList = {'1':'icon\icon_image_01.png', '2':'icon\icon_image_02.png', '3':'icon\icon_image_03.png', '4':'icon\icon_image_04.png'}
        floorTypeList = {'0':self.ui.img_main, '1':self.ui.img_satellite, '2':self.ui.img_telework}

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
                img_icon = PersonalIcon(floorTypeList[desk['RowKey'][0:1]], 20, img_path, user_name)
                img_icon.setGeometry(desk['x'], desk['y'], img_icon.width(), img_icon.height())
                gDeskStatusList.update({desk['RowKey']:{'user_id':user_id, 'user_name':user_name, 'icon':img_icon, 'x':desk['x'], 'y':desk['y']}})

        # 画面ロック解放前処理
        self.beforeReleaseScrLock()

        # 画面ロック解放
        gScrLock.release()


    #----------------------------------------------
    # （内部処理）自動画面更新
    #----------------------------------------------
    def autoUpdateScr(self):

        # 更新処理を1分毎に呼び出し
        while True:

            self.updateIcon()
            time.sleep(60)


    #----------------------------------------------
    # （内部処理）自動話し中フラグ更新
    #----------------------------------------------
    def autoUpdateIsSpeakingFlg(self):

        # 話し中判定処理を常に呼び出し
        while True:

            global gIsSpeakingFlg
            gIsSpeakingFlg = MyAudio.IsSpeaking()
            time.sleep(5)


    #----------------------------------------------
    # （イベント）メニュー表示
    #----------------------------------------------
    def aboutToShowMenu(self):

        # 画面更新をロック
        global gScrLock
        gScrLock.acquire()


    #----------------------------------------------
    # （イベント）メニュー非表示
    #----------------------------------------------
    def aboutToHideMenu(self):

        # 画面ロック解放前処理
        self.beforeReleaseScrLock()

        # 画面ロック解放
        global gScrLock
        gScrLock.release()


    #----------------------------------------------
    # （内部処理）画面ロック解放前処理
    #----------------------------------------------
    def beforeReleaseScrLock(self):

        # アイコンと画面を再描画する
        self.update()

        global gDeskStatusList
        if len(gDeskStatusList)>0:
            for deskInfo in gDeskStatusList.values():
                if not deskInfo['icon']==None:
                    deskInfo['icon'].repaint()

        self.repaint()

    #----------------------------------------------
    # （内部処理）終了処理
    #----------------------------------------------
    def _on_destroyed():

        # DB情報を初期化
        userId = ''
        userName = ''
        statusCd = ''
        MyCosmosDB.updateDeskStatus(const.DESK_ID, userId, userName, statusCd)

        # 一時保存写真を削除
        if os.path.exists('image\image.png'):
            os.remove('image\image.png')


if __name__ == '__main__':

    app = Qw.QApplication(sys.argv)         #パラメータは正しくはコマンドライン引数を与える
    wmain = MyForm()                        #MyFormのインスタンスを作って
    wmain.show()                            #表示する

    #　1分毎に自動更新するよう，マルチスレッドで処理
    # （自動更新を停止させる場合，以下をコメントアウトしてwmain.show()を復活させる）
    # （自動更新を復活させる場合，以下を復活させてwmain.show()をコメントアウトする）
    '''
    thread_1 = threading.Thread(target=wmain.show())
    thread_1.start()
    thread_2 = threading.Thread(target=wmain.autoUpdateScr)
    thread_3 = threading.Thread(target=wmain.autoUpdateIsSpeakingFlg)
    thread_2.setDaemon(True)    # 無限ループ処理のためデーモンスレッドに設定
    thread_3.setDaemon(True)    # 無限ループ処理のためデーモンスレッドに設定
    thread_2.start()
    thread_3.start()
    '''

    sys.exit(app.exec())                    #こうやって終了コードを渡して抜けるのが礼儀
