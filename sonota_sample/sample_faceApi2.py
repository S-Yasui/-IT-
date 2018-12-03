'''
import httplib3, urllib3, base64
import json

# Request header
headers = {
# Request headers
'Content-Type': 'application/json',
'Ocp-Apim-Subscription-Key': '0d376b5d65c1439eab3e06154da07cc8',
}

params = urllib3.urlencode({
# Request parameters
'returnFaceId': 'true',
'returnFaceLandmarks': 'true',
'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses',
})

image_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'

body = {
# Request body
'url': image_url
}

try:
    conn = httplib3.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    print(json.dumps(data, indent=4))
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
'''

import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

#### Request headers
#'Content-Type': APIに送るメディアのタイプ.
#  'application/json'(URL指定の場合), 'application/octet-stream' (Local ファイル転送の場合)
#'Ocp-Apim-Subscription-Key': APIキーを指定する
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '0d376b5d65c1439eab3e06154da07cc8',
}

#### Request parameters
# 取得したい情報について、パラメータを指定する
# 'returnFaceId': 入力した顔画像に付与されるIDを返すかどうか
# 'returnFaceLandmarks' : 目や口などの特徴となる部分の座標を返すかどうか
# 'returnFaceAttributes' :　認識した顔からわかる属性を返す
#   指定できるパラメータは以下で、コンマで分けて複数指定可能
#       age, gender, headPose, smile, facialHair,
#       glasses, emotion, hair, makeup, occlusion,
#       accessories, blur, exposure and noise
params = urllib.parse.urlencode({
    'returnFaceId': 'true',
#    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,smile,facialHair,emotion'
})

#### Request body
# 入力したい画像の指定をする. 画像URLの指定, local ファイルの指定から選択
# 画像はJPEG, PNG, GIF, BMPに対応
# サイズの上限は4MB
# 認識可能な顔のサイズは 36x36 - 4096x4096 pixelsの範囲
# 最大64個の顔を認識可能

## URL 指定の場合以下のコメントアウトを外し、image_urlを指定する
image_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
body = { 'url': image_url }
body = json.dumps(body)

## Local file指定の場合
# 以下の image_file_path に読み込むファイルのパスを指定する
#image_file_path = 'XXXXXXXX.jpeg'
#image_file = open(image_file_path,'rb')
#body = image_file.read()
#image_file.close()

#### API request
# 接続先リージョンによっては, 以下HTTPSConnection の "westus.api.cognitive.microsoft.com" 部分は変更する.
# この場合は「westus」なので北米西部リージョン
# なお "/face/v1.0/detect?%s" の部分が接続先APIの機能を指定している
try:
    conn = http.client.HTTPSConnection('japaneast.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    print(json.dumps(data, indent=4))
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
