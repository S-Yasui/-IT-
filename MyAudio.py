# -*- coding: utf-8 -*-

try:
    from PySide import QtWidgets
except:
    from PyQt5 import QtWidgets

import pyaudio
import numpy as np

import sys
import os
from ctypes import *
user32 = windll.user32

class MyAudio:

    #----------------------------------------------
    # （内部処理）話し声検知
    #----------------------------------------------
    def IsSpeaking():

        CHUNK = 1024
        FORMAT = pyaudio.paInt16    # int16型
        CHANNELS = 1                # モノラル
        RATE = 44100                # 441.kHz
        RECORD_SECONDS = 2          # 2秒間録音
        THRESHOLD = 0.5             # 閾値(ここを調整する)

        try:

            # pyAudioインスタンスを作成
            p = pyaudio.PyAudio()

            # ストリーム開始
            stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)

            # 返却値初期化
            ret = False

            # データを読み込み閾値を計算
            data = stream.read(CHUNK)
            x = np.frombuffer(data, dtype="int16") / 32768.0

            # 設定値以上の閾値なら話している（True）
            if x.max() > THRESHOLD:
                ret = True

            # ストリームを終了・破棄
            stream.stop_stream()
            stream.close()
            p.terminate()

            # 結果返却
            return ret

        except Exception as e:
            user32.MessageBoxW(0, '{0}:{1}'.format('IsSpeaking',e.args[0]), u'ERROR', 0x00000010)
            return False
