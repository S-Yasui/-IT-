#!/usr/bin/env python
#coding:utf-8
import sys
import os.path
from ctypes import *
user32 = windll.user32

import unicodedata
import re
from simple_tfidf_japanese.tfidf import TFIDF

if __name__ == '__main__':
    # 山本昌
    _base_url = "https://ja.wikipedia.org/wiki/%E5%B1%B1%E6%9C%AC%E6%98%8C"

    # 比較対象
    data = [
         ['ヤクルト', 'https://ja.wikipedia.org/wiki/%E6%9D%B1%E4%BA%AC%E3%83%A4%E3%82%AF%E3%83%AB%E3%83%88%E3%82%B9%E3%83%AF%E3%83%AD%E3%83%BC%E3%82%BA'],
         ['巨人', 'https://ja.wikipedia.org/wiki/%E8%AA%AD%E5%A3%B2%E3%82%B8%E3%83%A3%E3%82%A4%E3%82%A2%E3%83%B3%E3%83%84'],
         ['阪神', 'https://ja.wikipedia.org/wiki/%E9%98%AA%E7%A5%9E%E3%82%BF%E3%82%A4%E3%82%AC%E3%83%BC%E3%82%B9'],
         ['広島', 'https://ja.wikipedia.org/wiki/%E5%BA%83%E5%B3%B6%E6%9D%B1%E6%B4%8B%E3%82%AB%E3%83%BC%E3%83%97'],
         ['中日', 'https://ja.wikipedia.org/wiki/%E4%B8%AD%E6%97%A5%E3%83%89%E3%83%A9%E3%82%B4%E3%83%B3%E3%82%BA'],
         ['横浜', 'https://ja.wikipedia.org/wiki/%E6%A8%AA%E6%B5%9CDeNA%E3%83%99%E3%82%A4%E3%82%B9%E3%82%BF%E3%83%BC%E3%82%BA'],
         ['ソフバン', 'https://ja.wikipedia.org/wiki/%E7%A6%8F%E5%B2%A1%E3%82%BD%E3%83%95%E3%83%88%E3%83%90%E3%83%B3%E3%82%AF%E3%83%9B%E3%83%BC%E3%82%AF%E3%82%B9'],
         ['日ハム', 'https://ja.wikipedia.org/wiki/%E5%8C%97%E6%B5%B7%E9%81%93%E6%97%A5%E6%9C%AC%E3%83%8F%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%82%BF%E3%83%BC%E3%82%BA'],
         ['ロッテ', 'https://ja.wikipedia.org/wiki/%E5%8D%83%E8%91%89%E3%83%AD%E3%83%83%E3%83%86%E3%83%9E%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%BA'],
         ['西武', 'https://ja.wikipedia.org/wiki/%E5%9F%BC%E7%8E%89%E8%A5%BF%E6%AD%A6%E3%83%A9%E3%82%A4%E3%82%AA%E3%83%B3%E3%82%BA'],
         ['オリックス', 'https://ja.wikipedia.org/wiki/%E3%82%AA%E3%83%AA%E3%83%83%E3%82%AF%E3%82%B9%E3%83%BB%E3%83%90%E3%83%95%E3%82%A1%E3%83%AD%E3%83%BC%E3%82%BA'],
         ['楽天', 'https://ja.wikipedia.org/wiki/%E6%9D%B1%E5%8C%97%E6%A5%BD%E5%A4%A9%E3%82%B4%E3%83%BC%E3%83%AB%E3%83%87%E3%83%B3%E3%82%A4%E3%83%BC%E3%82%B0%E3%83%AB%E3%82%B9'],
         ['サッカー日本代表', 'https://ja.wikipedia.org/wiki/%E3%82%B5%E3%83%83%E3%82%AB%E3%83%BC%E6%97%A5%E6%9C%AC%E4%BB%A3%E8%A1%A8'],
    ]

    # 計算
    result = TFIDF.some_similarity(_base_url, data)

    # 結果表示
    result.sord(key=lambda x: x[2], reverse=True)
    for title, url, value in result:
         print(title, value)

