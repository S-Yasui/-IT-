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

import cv2
import sys
import os.path
from ctypes import *
user32 = windll.user32

class MyFaceApi:
    def __init__(self):
        pass

    #----------------------------------------------
    # （内部処理）顔検知
    #----------------------------------------------
    def DetectFaces(image_file_path):
        try:

            # APIキーのセット
            api_key = '0d376b5d65c1439eab3e06154da07cc8'
            CF.Key.set(api_key)

            BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
            CF.BaseUrl.set(BASE_URL)

            # リクエスト送信
            result = CF.face.detect(image_file_path)
            faceIds = []
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

            # APIキーのセット
            api_key = '0d376b5d65c1439eab3e06154da07cc8'
            CF.Key.set(api_key)

            BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
            CF.BaseUrl.set(BASE_URL)

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

            # APIキーのセット
            api_key = '0d376b5d65c1439eab3e06154da07cc8'
            CF.Key.set(api_key)

            BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
            CF.BaseUrl.set(BASE_URL)

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
            #image_file_path = 'C:/Users/user/Desktop/2社合同IT研究会/IT研究会資料/sonota_sample/img/image01.png'

            # 顔検知
            faceIds = MyFaceApi.DetectFaces(image_file_path)
            print(faceIds)

            # 顔検知エラー
            if faceIds == None:
                return None
            # 顔検知なし
            if len(faceIds)==0:
                return []

            # 顔識別
            identify_result = MyFaceApi.IdentifyFaces(faceIds)
            print(identify_result)

            #　顔認識エラー
            if identify_result == None:
                return None

            # 人物取得
            retList = MyFaceApi.GetPerson(identify_result)
            print(retList)
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
            cv2.imwrite('image/' + picFileName, image)
            break

        # キャプチャを解放する
        capture.release()
        return picFileName, msg
