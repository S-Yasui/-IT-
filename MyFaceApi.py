# -*- coding: utf-8 -*-

try:
    from PySide import QtWidgets
except:
    from PyQt5 import QtWidgets

import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import const
const.API_KEY = '0d376b5d65c1439eab3e06154da07cc8'
const.BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL

import cv2
import sys
import os
from ctypes import *
user32 = windll.user32

class MyFaceApi:

    #----------------------------------------------
    # （内部処理）顔検知
    #----------------------------------------------
    def DetectFaces(image_file_path):
        try:

            # APIキー，接続リージョンのセット
            CF.Key.set(const.API_KEY)
            CF.BaseUrl.set(const.BASE_URL)

            # 画像ファイルの存在確認
            if not os.path.exists(image_file_path):
                user32.MessageBoxW(0, '写真が存在しません。：{0}'.format(image_file_path), u'ERROR', 0x00000010)
                return None

            # リクエスト送信
            result = CF.face.detect(image_file_path)
            faceIds = []
            if len(result) > 0:
                for face in result:
                    faceIds.append(face['faceId'])

            return faceIds

        except Exception as e:
            user32.MessageBoxW(0, '{0}:{1}'.format('DetectFaces',e.args[0]), u'ERROR', 0x00000010)
            return None


    #----------------------------------------------
    # （内部処理）顔識別
    #----------------------------------------------
    def IdentifyFaces(faceIds):
        try:

            # APIキー，接続リージョンのセット
            CF.Key.set(const.API_KEY)
            CF.BaseUrl.set(const.BASE_URL)

            # 顔認識結果を返却
            groupId = 'test_group'
            return CF.face.identify(faceIds, person_group_id=groupId)

        except Exception as e:
            user32.MessageBoxW(0, '{0}:{1}'.format('IdentifyFaces',e.args[0]), u'ERROR', 0x00000010)
            return None


    #----------------------------------------------
    # （内部処理）人物取得
    #----------------------------------------------
    def GetPerson(identify_result):
        try:

            # APIキー，接続リージョンのセット
            CF.Key.set(const.API_KEY)
            CF.BaseUrl.set(const.BASE_URL)

            # 人物を取得
            personList = []
            groupId = 'test_group'
            for ret in identify_result:
                if len(ret['candidates'])==0:
                    # 顔認識結果：当てはまる人物がいない場合
                    personList.append({'userId':'Unknown','userName':'Unknown'})
                else:
                    # 当てはまる人物が存在する場合
                    candidates = ret['candidates'][0]
                    result = CF.person.get(groupId, candidates['personId'])
                    if len(result)==0:
                        personList.append({'userId':'Unknown','userName':'Unknown'})
                    else:
                        personList.append({'userId':result['userData'],'userName':result['name']})

            return personList

        except Exception as e:
            user32.MessageBoxW(0, '{0}:{1}'.format('GetPerson',e.args[0]), u'ERROR', 0x00000010)
            return None


    #----------------------------------------------
    # （内部処理）人物情報取得
    #----------------------------------------------
    def getPersonInfo():
        try:

            retList = []

            # Webカメラで写真を撮影してローカルに保存
            image_file_name, msg = MyFaceApi.CapturePic()
            if not msg == '':
                # 写真保存エラーの場合
                user32.MessageBoxW(0, msg, u'ERROR', 0x00000010)
                return None

            image_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'image',image_file_name)

            # 顔検知
            faceIds = MyFaceApi.DetectFaces(image_file_path)

            # 顔検知エラー
            if faceIds == None:
                return None
            # 顔検知なし
            if len(faceIds)==0:
                return []

            # 顔識別
            identify_result = MyFaceApi.IdentifyFaces(faceIds)

            #　顔認識エラー
            if identify_result == None:
                return None

            # 人物取得
            retList = MyFaceApi.GetPerson(identify_result)
            return retList

        except Exception as e:
            user32.MessageBoxW(0, '{0}:{1}'.format('getPersonInfo',e.args[0]), u'ERROR', 0x00000010)
            return None


    #----------------------------------------------
    # （内部処理）写真撮影
    #----------------------------------------------
    def CapturePic():

        # 返却値を初期化
        picFileName = ''
        msg = ''

        # VideoCaptureクラスをインスタンス化
        capture = cv2.VideoCapture(0)

        # Webカメラの接続確認
        if capture.isOpened() == False:
            msg = 'Webカメラに接続されていません。'
            capture.release()
            return picFileName, msg

        tryCount = 0

        while True:

            # Webカメラから画像読込
            ret, image = capture.read()

            if ret == False:
                # 3回まで試行
                if tryCount >= 3:
                    msg = 'Webカメラの画像読込に失敗しました。'
                    break

                tryCount = tryCount + 1
                continue

            # 画像を保存して処理を抜ける
            picFileName = 'image.png'

            # フォルダが存在しない場合作成する
            if not os.path.exists('image'):
                os.mkdir('image')

            cv2.imwrite('image/' + picFileName, image)
            break

        # キャプチャを解放する
        capture.release()
        return picFileName, msg
