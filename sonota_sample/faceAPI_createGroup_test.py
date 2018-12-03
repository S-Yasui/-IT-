#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cognitive_face as CF
import json

# APIキーのセット
api_key = '0d376b5d65c1439eab3e06154da07cc8'
CF.Key.set(api_key)

BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# Person Groupの作成
GroupId = 'test_group'
GroupName = 'test_group'
#CF.person_group.create(GroupId, name=GroupName)

# Person Groupの確認
print(json.dumps(CF.person_group.get(GroupId), indent = 4))
