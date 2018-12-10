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
import json
import io
import const

import mysrcdialog as mysrcdialog               #デザイナーで作った画面をインポートする


class MySearchDialog(Qw.QDialog):               #QDialog

    # クラス変数
    srcIndex = -1

    #----------------------------------------------
    # （内部処理）初期化処理
    #----------------------------------------------
    def __init__(self, parent=None, srcList=None):        #クラスの初期化

        super().__init__(parent)            #上位クラスの初期化ルーチンを呼び出す（補足2）
        self.ui = mysrcdialog.Ui_Dialog()   #先ほど作ったhello.pyの中にあるクラスの
        self.ui.setupUi(self)               #このコマンドを実行する
        const.srcList = srcList

        # クラス変数初期化
        global srcIndex
        srcIndex = -1


    #----------------------------------------------
    # （イベント）検索
    #----------------------------------------------
    def search(self):

        srcText = self.ui.srcText.text()

        if len(srcText)==0:
            user32.MessageBoxW(0, '検索文字列を入力してください。', u'WARNING', 0x00000030)
            return

        for deskInfo in const.srcList.values():
            deskInfo['icon'].setOpacity(0.3)

        global srcIndex
        # 最後まで検索されていた場合は先頭から
        if srcIndex >= len(const.srcList)-1:
            srcIndex = -1

        # 最後にヒットしたインデックスを保存
        lastHitIndex = srcIndex

        for ind, deskInfo in enumerate(const.srcList.values()):

            srcIndex = ind

            if ind <= lastHitIndex:
                # 最後にヒットしたインデックスより後を検索する
                pass
            else:
                userName = deskInfo['user_name']
                if not userName == None:
                    if userName.count(srcText):
                        deskInfo['icon'].setOpacity(1.0)
                        return

        # 見つからない場合，先頭から再検索
        if lastHitIndex > -1:
            for ind, deskInfo in enumerate(const.srcList.values()):
                srcIndex = ind
                userName = deskInfo['user_name']
                if not userName == None:
                    if userName.count(srcText):
                        deskInfo['icon'].setOpacity(1.0)
                        return

        user32.MessageBoxW(0, '見つかりませんでした。', u'WARNING', 0x00000030)


    #----------------------------------------------
    # （イベント）すべて検索
    #----------------------------------------------
    def searchAll(self):

        # 検索文字列
        srcText = self.ui.srcText.text()

        if len(srcText)==0:
            user32.MessageBoxW(0, '検索文字列を入力してください。', u'WARNING', 0x00000030)
            return

        hitFlg = False
        for deskInfo in const.srcList.values():

            # ユーザ情報を取得
            userName = deskInfo['user_name']

            if not userName == None:
                if userName.count(srcText):
                    # ユーザ名に検索文字列が含まれている場合
                    deskInfo['icon'].setOpacity(1.0)
                    hitFlg = True
                else:
                    # ユーザ名に検索文字列が含まれていない場合
                    deskInfo['icon'].setOpacity(0.3)

        if not hitFlg:
            user32.MessageBoxW(0, '見つかりませんでした。', u'WARNING', 0x00000030)


    #----------------------------------------------
    # （イベント）検索インデックス再設定
    #----------------------------------------------
    def resetSearchIndex(self):
        global srcIndex
        srcIndex = -1
