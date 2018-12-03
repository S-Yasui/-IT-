#!/usr/bin/env python
#coding:utf-8

import cognitive_face as CF

KEY = '0d376b5d65c1439eab3e06154da07cc8'
CF.Key.set(KEY)

img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
result = CF.face.detect(img_url)
print(result)
