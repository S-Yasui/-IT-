#!/usr/bin/env python
#coding:utf-8

import cv2
import sys

if __name__=="__main__":

    # VideoCaptureクラスをインスタンス化
    capture = cv2.VideoCapture(0)

    # Webカメラの接続確認
    if capture.isOpened() == False:
        print("Webカメラに接続されていません。")
        sys.exit()

    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)

    while True:

        ret, image = capture.read()

        if ret == False:
            continue

        cv2.imshow("Capture", image)

        # 何かキー入力があった場合，画像を保存して処理を抜ける
        if cv2.waitKey(33) >= 0:
            cv2.imwrite("image.png", image)
            break

    # キャプチャを解放する
    capture.release()
    cv2.destroyAllWindows()
