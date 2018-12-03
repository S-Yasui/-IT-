#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
from ctypes import *
user32 = windll.user32
import re

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfparser import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFPage
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal

'''
space = re.compile(u"[ 　]+")

class PdfMinerSample(object):

    def __init__(self):
        pass

    def convert_pdf_to_txt(path, txtname, buf=True):
        rsrcmgr = PDFResourceManager()
        if buf:
            outfp = StringIO()
        else:
            outfp = open(txtname, 'w')
        codec = 'utf-8'
        laparams = LAParams()
        laparams.detect_vertical = True
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)

        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        fp.close()
        device.close()
        if buf:
            text = re.sub(space, "", outfp.getvalue())
            print(text)
        outfp.close()
'''

#----------------------------------------
# 主処理
#----------------------------------------
if __name__ == '__main__':

    print(u'開始')

    fp = open('20090319【受託管理】①概要説明資料(機密2).pdf', 'rb')

    parser = PDFParser(fp)
    document = PDFDocument()
    parser.set_document(document)

    password='' # pdfを開くときのパスワード
    document.set_parser(parser) # set parser to document
    document.initialize(password)

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    pages = list(document.get_pages())

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
                print(l.get_text()) # オブジェクト中のtextのみ抽出
