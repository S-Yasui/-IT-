#!/usr/bin/env python
#coding:utf-8

import pyaudio
import wave
import numpy as np
from datetime import datetime

# 一定以上の音量を2秒間録音してwavファイルを作成する

CHUNK = 1024
FORMAT = pyaudio.paInt16    # int16型
CHANNELS = 1                # モノラル
RATE = 44100                # 441.kHz
RECORD_SECONDS = 2          # 2秒間録音
THRESHOLD = 0.01            # 閾値(ここを調整する)

# pyAudioインスタンスを作成
p = pyaudio.PyAudio()

# ストリーム開始
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)

while True:

    # データを読み込み閾値を計算
    data = stream.read(CHUNK)
    x = np.frombuffer(data, dtype="int16") / 32768.0

    # 設定値以上の閾値なら5秒間録音
    if x.max() > THRESHOLD:

        # ファイル名を設定
        filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".wav"
        print(filename)

        # 2秒間録音
        frames = []
        for i in range(0, int(RATE / CHUNK * int(RECORD_SECONDS))):
            data = stream.read(CHUNK)
            frames.append(data)

        # wavファイルを作成
        out = wave.open(filename,'w')               # ファイルオープン
        out.setnchannels(CHANNELS)                  # モノラル
        out.setsampwidth(p.get_sample_size(FORMAT)) # サンプリング周波数
        out.setframerate(RATE)                      # フレーム数
        out.writeframes(frames)                     # データをファイルに書き込み
        out.close()                                 # ファイルクローズ

        print("Saved.")

    # key入力待ち：引数はウェイト時間(ms)：0だと無限に待つ
    inkey = cv2.waitKey(1)
    if  inkey == 0x1b:
        #ESCで終了
        break

# ストリームを終了・破棄
stream.stop_stream()
stream.close()
p.terminate()
