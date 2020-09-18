#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: yinbo.qiao
# File: test.py
# datetime: 2020/9/3 21:03
# software: PyCharm

from selenium import webdriver
from quanze_list.util import *

url = 'http://zwfw.guizhou.gov.cn/eptemp.aspx?t=Znzw.bgt_Html.bgt_html.bgt_bmqjd&istest=1&ocode=-4188128443937240449&orgcode=35070&areacode=520000'
browser = webdriver.PhantomJS()
browser.get(url)
with open('phantomjs.txt','w+',encoding='utf-8') as f:
    f.write(browser.page_source)
if nextPage(browser,browser.page_source)==1:
    with open('phantomjs2.txt','w+',encoding='utf-8') as f:
        f.write(browser.page_source)
else:
    print('error')