#!/usr/bin/env python
#coding:utf-8

import cv2
import time
import numpy as np


fonts = (cv2.FONT_HERSHEY_COMPLEX,
         cv2.FONT_HERSHEY_COMPLEX_SMALL,
         cv2.FONT_HERSHEY_DUPLEX,
         cv2.FONT_HERSHEY_PLAIN,
         cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
         cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
         cv2.FONT_HERSHEY_SIMPLEX,
         cv2.FONT_HERSHEY_TRIPLEX,
         cv2.FONT_ITALIC)

myFilter1 = np.array([[-1,-1,-1,-1,-1,-1,-1],
                      [-1, 0, 0, 0, 0, 0,-1],
                      [-1, 0, 0, 0, 0, 0,-1],
                      [-1, 0, 0,26, 0, 0,-1],
                      [-1, 0, 0, 0, 0, 0,-1],
                      [-1, 0, 0, 0, 0, 0,-1],
                      [-1,-1,-1,-1,-1,-1,-1]], np.float32) / 2.0

myFilter2 = np.array([[-1,-1,-1,-1,-1,-1,-1],
                      [-1, 0, 0, 0, 0, 0,-1],
                      [-1, 0, 0, 0, 0, 0,-1],
                      [-1, 0, 0,24, 0, 0,-1],
                      [-1, 0, 0, 0, 0, 0,-1],
                      [-1, 0, 0, 0, 0, 0,-1],
                      [-1,-1,-1,-1,-1,-1,-1]], np.float32) / 2.0

myFilterAve7 = np.ones((7, 7),np.float32) / 49.0

def thru(img):

    # 何も加工しない生画像
    return img

def edge(img):

    # エッヂ検出：パラメータは適当
    tmp = cv2.Canny(img, 100, 200)
    return tmp

def oil_paint(img):

    # 油絵調
    # メディアンフィルタ
    tmp = cv2.medianBlur(img, 11)

    # 輪郭強調
    tmp = cv2.filter2D(tmp, -1, myFilter1)

    # ざらつきを無くしたいなら好みの回数だけ3x3medianフィルタ
    for i in range(1):
        tmp = cv2.medianBlur(tmp, 3)
    return tmp

def hanga1(img):

    # まず油絵調化
    op = oil_paint(img)

    # 油絵調の画像をgrayscale化
    gray = cv2.cvtColor(op, cv2.COLOR_BGR2GRAY)

    # 平均輝度算出
    ave = np.average(gray)

    # ２値化
    ret, hanga1 = cv2.threshold(gray, ave, 255, cv2.THRESH_BINARY)

    return hanga1

def hanga2(img):

    # 版画２

    # 7*7の平滑化
    tmp = cv2.filter2D(img, -1, myFilterAve7)

    # grayscale化
    tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)

    # 輪郭抽出*3回
    tmp = cv2.filter2D(tmp, -1, myFilter2)
    tmp = cv2.filter2D(tmp, -1, myFilter2)
    tmp = cv2.filter2D(tmp, -1, myFilter2)

    return tmp


# 最初はmode=0(生画像)を表示

modes = [thru, edge, oil_paint, hanga1, hanga2]
modeN = len(modes)
mode  = 0

if __name__=="__main__":

    # VideoCaptureクラスのインスタンス生成：引数はカメラ番号
    capture = cv2.VideoCapture(0)

    # Hight,Width,fpsのパラメータはwebcamによっては効かない
    capture.set(3, 640)  # Width
    capture.set(4, 480)  # Height
    capture.set(5, 15)   # fps

    # カメラに接続できていなければ終了
    if capture.isOpened() is False:
        print("Webカメラに接続されていません。")
        sys.exit()

    # fps計測用初期値設定
    counter = 0
    fps = 0
    startTime = time.time()

    # MainRoutine

    while (capture.isOpened()):

        #---- start of Loop ------------------------------------

        # キャプチャ
        ret, image = capture.read()

        # もし正常にキャプチャできなければ後の処理を省略
        if ret == False:
            continue

        # fps算出：小数点以下1桁
        counter += 1
        counter %= 60
        if counter == 0:
            nowTime = time.time()
            fps = round(60 / (nowTime - startTime), 1)
            startTime = nowTime

        # modeに応じた加工
        image = modes[mode](image)

        # fpsをimageに描画：fontとかsizeとかはお好みで
        startXY = (0, 30)
        font = fonts[8]
        size = 1
        color = (255, 0, 0)
        cv2.putText(image, str(fps), startXY, font, size, color)

        # windowに表示
        cv2.imshow("Capture", image)

        # key入力待ち：引数はウェイト時間(ms)：0だと無限に待つ
        inkey = cv2.waitKey(1)
        if  inkey == 0x1b:
            #ESCで終了
            break
        elif (inkey==ord('s')) or (inkey==ord('S')):
            # Sキーで画像保存
            cv2.imwrite("image.png", image)
        elif inkey >= 0:
            # それ以外の入力があったならmode変更
            mode = (mode + 1) % modeN

        #---- end of Loop ------------------------------------


    # ここでインスタンスを開放しないと2回目の起動でこける
    capture.release()

    # 全てのウィンドウを破棄して終了
    cv2.destroyAllWindows()
