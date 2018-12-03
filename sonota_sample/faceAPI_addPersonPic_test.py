#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cognitive_face as CF
import json

# APIキーのセット
api_key = '0d376b5d65c1439eab3e06154da07cc8'
CF.Key.set(api_key)

BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# 顔の追加
groupId = 'test_group'
personId = '1e1ae1a8-c384-4143-b26f-9ffa1ae1bea4'
image_file_path = 'C:/Users/user/Desktop/2社合同IT研究会/IT研究会資料/sonota_sample/img/faceOnly/image06.png'
#image_file = open(image_file_path,'rb')
#stream = image_file.read()
#image_file.close()

#CF.person.add_face(image_file_path, groupId, personId)

# Personの確認
print(json.dumps(CF.person.get(groupId, personId), indent = 4))
