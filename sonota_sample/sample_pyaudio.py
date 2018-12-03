#!/usr/bin/env python
#coding:utf-8

import pyaudio
import wave
from datetime import datetime

# 開始から5秒間録音してwavファイルを作成する

CHUNK = 1024
FORMAT = pyaudio.paInt16 # int16型
CHANNELS = 2             # ステレオ
RATE = 44100             # 441.kHz
RECORD_SECONDS = 5       # 5秒録音
WAVE_OUTPUT_FILENAME = datetime.today().strftime("%Y%m%d%H%M%S") + ".wav"   # ファイル名

# pyAudioインスタンスを作成
p = pyaudio.PyAudio()

# ストリーム開始
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    # 2秒間データを読み込んでframesに追加する
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

# ストリームを終了・破棄
stream.stop_stream()
stream.close()
p.terminate()

# wavファイルを作成・保存
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # ファイルオープン
wf.setnchannels(CHANNELS)                   # ステレオ
wf.setsampwidth(p.get_sample_size(FORMAT))  # サンプリング周波数
wf.setframerate(RATE)                       # フレーム数
wf.writeframes(b''.join(frames))            # frames（録音データ）をファイルに書き込み
wf.close()                                  # ファイルクローズ
