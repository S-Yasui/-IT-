#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
from ctypes import *
user32 = windll.user32

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfparser import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFPage
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal

import unicodedata
import re
from simple_tfidf_japanese.tfidf import TFIDF

class PdfMinerSample(object):

    def __init__(self):
        pass

    #----------------------------------------
    # pdfをテキスト変換
    #----------------------------------------
    def convert_pdf_to_txt(pPath, pPassword):
        fp = open(pPath, 'rb')

        parser = PDFParser(fp)
        document = PDFDocument()
        parser.set_document(document)

        document.set_parser(parser)     # set parser to document
        document.initialize(pPassword)  # pdfを開くときのパスワード

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        pages = list(document.get_pages())

        textList = []
        for page in pages:

            # interpreter page
            interpreter.process_page(page)

            # receive the LTPage object for the page.
            # layoutの中にページを構成する要素（LTTextBoxHorizontalなど）が入っている
            layout = device.get_result()
            # print(layout)

            for l in layout:
            #     print(l) # l is object
                if isinstance(l, LTTextBoxHorizontal):
                    textList.append(l.get_text()) # オブジェクト中のtextのみ抽出

        fp.close()

        return ''.join(textList)

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
    # tfidf出力
    #----------------------------------------
    def getTfidf(pText):

       t = TFIDF.gen(pText, enable_one_char=1)

       cnt = 0
       for key, value in t:
           if cnt >= 10:
               break

           print(key, value)
           cnt = cnt + 1

    #----------------------------------------
    # tfidf類似度計算
    #----------------------------------------
    def getTfidfSimilarity(pText1, pText2):

        t1 = TFIDF.gen(pText1, enable_one_char=1)
        t2 = TFIDF.gen(pText2, enable_one_char=1)

        # 類似度計算
        return TFIDF.similarity(t1, t2)


#----------------------------------------
# 主処理
#----------------------------------------
if __name__ == '__main__':

    print(u'開始')

    file1 = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts/20090319【受託管理】①概要説明資料(機密2).pdf'
    file2 = 'C:/Users/S7223/Documents/03_目標管理/Python Scripts/20090319【受託管理】③実績入力許可確認申請一覧_兼_契約状況確認一覧(機密2).pdf'

    text1 = PdfMinerSample.convert_pdf_to_txt(file1, '')
    text2 = PdfMinerSample.convert_pdf_to_txt(file2, '')

    text1 = PdfMinerSample.shapeText(text1)
    text2 = PdfMinerSample.shapeText(text2)

    keyWord = '概要　契約'

    print(file1)
    PdfMinerSample.getTfidf(text1)

    print('')
    print(file2)
    PdfMinerSample.getTfidf(text2)

    print('')
    print(keyWord)
    print('')
    sim1 = PdfMinerSample.getTfidfSimilarity(text1, keyWord)
    print(sim1)
    sim2 = PdfMinerSample.getTfidfSimilarity(text2, keyWord)
    print(sim2)

    if sim1 > sim2:
        print(file1)
    else:
        print(file2)




