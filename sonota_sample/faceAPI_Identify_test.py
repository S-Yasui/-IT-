#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cognitive_face as CF
import json

# APIキーのセット
api_key = '0d376b5d65c1439eab3e06154da07cc8'
CF.Key.set(api_key)

BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# 顔検出
image_file_path = 'C:/Users/user/Desktop/2社合同IT研究会/IT研究会資料/image/test_01.png'
detect_result = CF.face.detect(image_file_path)
print(detect_result)

if len(detect_result) == 0:
    print('No one detected')
    sys.exit()

# Face Idのリストを作成
idList = []
for rst in detect_result:
    idList.append(rst['faceId'])

# 顔認識
groupId = 'test_group'
identify_result = CF.face.identify(idList, person_group_id=groupId)

if len(identify_result) == 0:
    print('Unknown')
    sys.exit()

print(identify_result)

# 人物情報を取得
for rst in identify_result:
    if len(rst['candidates']) > 0:
        candidates = rst['candidates'][0]
        getPersonResult = CF.person.get(groupId, candidates['personId'])
        print(getPersonResult)

