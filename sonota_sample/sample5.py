#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
from ctypes import *
user32 = windll.user32
import subprocess
import unicodedata
import re
from janome.tokenizer import Tokenizer
from simple_tfidf_japanese.tfidf import TFIDF
from janome.dic import UserDictionary
import sysdic

class JanomeSample(object):

    def __init__(self):
        pass

    #----------------------------------------
    # ファイル読み込み処理
    #----------------------------------------
    def readFile(pFileName):

        # nkfで文字コードを判別
        cmd = 'nkf -g %s' % (os.path.basename(pFileName))
        ecd = subprocess.check_output(cmd,shell=True).decode(encoding='UTF-8')

        # ファイル読み込み
        f = open(pFileName, 'r', encoding=ecd)

        try:
            with f:
               text = f.read()
        except:
            e = sys.exc_info()[1]
            #例外処理
            user32.MessageBoxW(0, '{}{}'.format(u'ファイルの読み込みに失敗しました。：',e.args[0]), u'ERROR', 0x00000010)
            return ""

        return text

    #----------------------------------------
    # 文章整形
    #----------------------------------------
    def shapeText(pText):

        #返却値
        text = pText

        # 改行コードを統一
        text = text.replace('\r\n','\n')
        text = text.replace('\r','\n')

        # 全角/半角を統一
        text = unicodedata.normalize('NFKC', text)

        # HTMLタグを取り除く
        htmltag = re.compile(r'<.*?>', re.I | re.S)
        text = htmltag.sub('', text)

        # 不要な記号を取り除く
        text = re.sub(r'&.*?;', '', text)
        text = text.replace('#','')
        text = text.replace(' ','')
        text = text.replace('　','')

        # 改行コードを全削除
        text = text.replace('\n','')
        # 「。」で一文とし，改行する
        text = text.replace('。','。\n')

        return text

    #----------------------------------------
    # ユーザ辞書コンパイル
    #----------------------------------------
    def compileUserDic(pInput, pOutput):

        user_dict = UserDictionary(pInput, "utf8", "ipadic", sysdic.connections)
        user_dict.save(pOutput)

    #----------------------------------------
    # 形態素解析
    #----------------------------------------
    def morphologicalAnalysis(pText, pUserDic):

        t = Tokenizer(userDic)

        for token in t.tokenize(pText):
            print(token.part_of_speech)

    #----------------------------------------
    # tfidf出力
    #----------------------------------------
    def getTfidf(pText):

       t = TFIDF.gen(pText, enable_one_char=1)
       for key, value in t:
            print(key, value)

    #----------------------------------------
    # tfidf類似度計算
    #----------------------------------------
    def getTfidfSimilarity(pText1, pText2):

        t1 = TFIDF.gen(pText1, enable_one_char=1)
        t2 = TFIDF.gen(pText2, enable_one_char=1)

        # 類似度計算
        print(TFIDF.similarity(t1, t2))

#----------------------------------------
# 主処理
#----------------------------------------
if __name__ == '__main__':

    print(u'開始')

    # 入力ファイル
    file1 = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts/HTMLsample4.txt'

    # ファイル読込
    print(u'ファイル読み込み中・・・')
    text = JanomeSample.readFile(file1)

    # 読み込んだテキストを整形
    print(u'テキスト整形中・・・')
    text = JanomeSample.shapeText(text)
    print(text)

    # TFIDF計算
    tfidf = TFIDF.gen(text, enable_one_char=1)

    # 上位5個のキーワードを決定
    keyWords = []
    for key, value in tfidf:
        if len(keyWords) < 5:
            keyWords.append([key, value])
            print(key, value)

    simAve = []
    for line in text.split('\n'):
        ts = 0.0
        # 各キーワードとの類似度を計算
        for k in keyWords:
            t1 = TFIDF.gen(line, enable_one_char=1)
            t2 = TFIDF.gen(k[0], enable_one_char=1)
            s = TFIDF.similarity(t1, t2)
            ts = ts + (s * k[1])

            simAve.append([line, ts])

    simAve.sort(key=lambda x:x[1], reverse=True)
    print(simAve[0])
    print(simAve[1])
    print(simAve[2])
