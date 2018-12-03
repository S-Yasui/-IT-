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
    # 接続判定処理
    #----------------------------------------
    def isConnectWords(pToken, pTmpToken):

        # 単語がすべてひらがなで構成されていたら接続しない
        if JanomeSample.isHiragana(pToken.surface):
            return False

        # 接頭詞は次に名詞が来たら接続する
        if (pTmpToken.part_of_speech.find(u'接頭詞') >= 0) and (pToken.part_of_speech.find(u'名詞') >= 0):
            return True

        # 接尾辞は一つ前に名詞，または動詞の連用形が来たら接続する
        if (pTmpToken.part_of_speech.find(u'名詞') >= 0) and (pToken.part_of_speech.find(u'接尾') >= 0):
            return True

        if (pTmpToken.part_of_speech.find(u'動詞') >= 0) and (pTmpToken.infl_form.find(u'連用形') >= 0) and (pToken.part_of_speech.find(u'接尾') >= 0):
            return True

        # 数字の次に助数詞が来たら接続する
        if (pTmpToken.part_of_speech.find(u'助数詞') >= 0) and (pToken.part_of_speech.find(u'数') >= 0):
            return True

        # 接頭詞,数接続 の次に数字が来たら接続する
        if (pTmpToken.part_of_speech.find(u'接頭詞') >= 0) and (pTmpToken.part_of_speech.find(u'数接続') >= 0) and (pToken.part_of_speech.find(u'数') >= 0):
            return True

    #----------------------------------------
    # ひらがな判定
    #----------------------------------------
    def isHiragana(pWord):
        for ch in pWord:
            if (ch < u'ぁ' or ch > u'ん') and ch != '_':
                return False

        return True

    #----------------------------------------
    # 単語接続
    #----------------------------------------
    def connectWords(pToken, pTmpToken, pNewWord):

        newSurface = ''
        newReading = ''
        newPhonetic = ''

        # 単語を接続して返却
        if len(pNewWord) > 0:
            #　単語
            newSurface = '{}{}'.format(pNewWord[0], pToken.surface)
            # 読み
            newReading = '{}{}'.format(pNewWord[1], pToken.reading)
            # 発音
            newPhonetic = '{}{}'.format(pNewWord[2], pToken.phonetic)
        else:
            #　単語
            newSurface = '{}{}'.format(pTmpToken.surface, pToken.surface)
            # 読み
            newReading = '{}{}'.format(pTmpToken.reading, pToken.reading)
            # 発音
            newPhonetic = '{}{}'.format(pTmpToken.phonetic, pToken.phonetic)

        return newSurface,newReading,newPhonetic


#----------------------------------------
# 主処理
#----------------------------------------
if __name__ == '__main__':

    print(u'開始')

    '''
    # ファイル名定義
    file1 = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts/HTMLsample.txt'
    file2 = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts/HTMLsample2.txt'

    #　ユーザ辞書コンパイル
    input = 'UserDic.csv'
    output = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts'
    JanomeSample.compileUserDic(input, output)

    # 整形した文書を形態素解析
    #line = u'太郎は花子が読んでいる本を次郎に渡した。'
    #line = u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
    #line = u'とうきょうすかいつりーへのおこしはとうぶすかいつりーらいんとうきょうすかいつりーえきがべんりです'
    line = u'飲み放題'

    # janome
    userDic = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts'
    JanomeSample.morphologicalAnalysis(line, userDic)
    '''


    # 入力ファイル
    file1 = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts/HTMLsample.txt'

    # ファイル読込
    print(u'ファイル読み込み中・・・')
    text = JanomeSample.readFile(file1)

    # 読み込んだテキストを整形
    print(u'テキスト整形中・・・')
    text = JanomeSample.shapeText(text)

    #　ユーザ辞書コンパイル
    print(u'ユーザ辞書コンパイル中・・・')
    input = 'UserDic.csv'
    output = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts'
    JanomeSample.compileUserDic(input, output)

    # 1行ずつ形態素解析
    print(u'形態素解析中・・・')
    userDic = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts'
    t = Tokenizer(userDic)
    tmpToken = None
    newWord = []
    newWordList = []

    for line in text.split('\n'):

        for token in t.tokenize(line):

            # 一時tokenがNoneの場合
            if tmpToken is None:
                # 現在の単語を一時保存して次のループへ
                tmpToken = token
                continue

            # 接続するか判定
            if JanomeSample.isConnectWords(token, tmpToken):
                # 接続する
                newWord = JanomeSample.connectWords(token, tmpToken, newWord)

                # 現在の単語を一時保存して次のループへ
                tmpToken = token
                continue

            else:
                # 接続しない
                if len(newWord) > 0:
                    #　新語がリストに登録されていない，かつ新語が全文章中に2回以上出現する
                    if (not newWord in newWordList) and (text.count(newWord[0])>=2):
                        # 新語をリストに登録
                        newWordList.append(newWord)

                #　新語と一時tokenを初期化
                newWord = []
                tmpToken = None

    print(newWordList)
